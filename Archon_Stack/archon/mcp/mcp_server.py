from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Archon MCP Server",
    description="Model Context Protocol server for Archon agent builder",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: str = Field(default="gpt-4-turbo-preview")
    temperature: float = Field(default=0.7)
    max_tokens: Optional[int] = Field(default=None)
    stream: bool = Field(default=False)

class ChatResponse(BaseModel):
    role: str
    content: str

class ErrorResponse(BaseModel):
    error: str

# Helper functions
async def get_openai_response(request: ChatRequest) -> ChatResponse:
    """Get response from OpenAI API"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": request.model,
                "messages": [{"role": m.role, "content": m.content} for m in request.messages],
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
                "stream": request.stream
            }
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        return ChatResponse(
            role=data["choices"][0]["message"]["role"],
            content=data["choices"][0]["message"]["content"]
        )

async def get_anthropic_response(request: ChatRequest) -> ChatResponse:
    """Get response from Anthropic API"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Anthropic API key not configured")

    # Convert model name if needed
    model = "claude-3-opus-20240229" if request.model == "gpt-4-turbo-preview" else request.model

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": model,
                "messages": [{"role": m.role, "content": m.content} for m in request.messages],
                "max_tokens": request.max_tokens or 4096,
                "temperature": request.temperature,
                "stream": request.stream
            }
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        return ChatResponse(
            role="assistant",
            content=data["content"][0]["text"]
        )

async def get_ollama_response(request: ChatRequest) -> ChatResponse:
    """Get response from Ollama API"""
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://ollama-cpu:11434")
    
    # Convert model name if needed
    model_mapping = {
        "gpt-4-turbo-preview": "qwen2.5-coder:7b",
        "gpt-3.5-turbo": "llama2-uncensored:7b",
        "claude-3-opus-20240229": "dolphin-mistral:7b"
    }
    model = model_mapping.get(request.model, request.model)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ollama_url}/api/chat",
            json={
                "model": model,
                "messages": [{"role": m.role, "content": m.content} for m in request.messages],
                "stream": request.stream
            }
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        data = response.json()
        return ChatResponse(
            role="assistant",
            content=data["message"]["content"]
        )

# Routes
@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """
    Get a chat completion from the configured model provider
    """
    try:
        # Try OpenAI first
        if os.getenv("OPENAI_API_KEY"):
            return await get_openai_response(request)
        # Then try Anthropic
        elif os.getenv("ANTHROPIC_API_KEY"):
            return await get_anthropic_response(request)
        # Finally, fall back to Ollama
        else:
            return await get_ollama_response(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

@app.get("/v1/models")
async def list_models():
    """
    List available models
    """
    models = [
        {
            "id": "gpt-4-turbo-preview",
            "name": "GPT-4 Turbo",
            "provider": "openai",
            "requires_key": True
        },
        {
            "id": "claude-3-opus-20240229",
            "name": "Claude 3 Opus",
            "provider": "anthropic",
            "requires_key": True
        },
        {
            "id": "qwen2.5-coder:7b",
            "name": "Qwen 2.5 Coder 7B",
            "provider": "ollama",
            "requires_key": False
        },
        {
            "id": "llama2-uncensored:7b",
            "name": "Llama 2 Uncensored 7B",
            "provider": "ollama",
            "requires_key": False
        },
        {
            "id": "dolphin-mistral:7b",
            "name": "Dolphin Mistral 7B",
            "provider": "ollama",
            "requires_key": False
        }
    ]
    return {"models": models}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8200) 
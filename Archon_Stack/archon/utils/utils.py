import os
from typing import Tuple, Optional
from openai import OpenAI
from supabase import create_client, Client
import streamlit as st
import httpx

def get_clients() -> Tuple[Optional[OpenAI], Optional[Client]]:
    """
    Initialize OpenAI and Supabase clients
    """
    # Initialize OpenAI client if API key is available
    openai_client = None
    if os.getenv("OPENAI_API_KEY"):
        openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Initialize Supabase client if URL and key are available
    supabase_client = None
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    if supabase_url and supabase_key:
        # Create a custom httpx client with SSL verification options
        transport = httpx.HTTPTransport(verify=True)
        client = httpx.Client(transport=transport)
        
        try:
            supabase_client = create_client(
                supabase_url,
                supabase_key,
                options={
                    "httpx_client": client,
                    "headers": {
                        "X-Client-Info": "supabase-py/2.16.0"
                    }
                }
            )
        except Exception as e:
            st.error(f"Failed to initialize Supabase client: {str(e)}")
            # Fallback to try without custom SSL settings
            try:
                supabase_client = create_client(supabase_url, supabase_key)
            except Exception as e:
                st.error(f"Failed to initialize Supabase client (fallback): {str(e)}")

    return openai_client, supabase_client

def check_environment() -> dict:
    """
    Check the environment configuration and return status
    """
    status = {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
        "supabase": bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY")),
        "ollama": bool(os.getenv("OLLAMA_BASE_URL", "http://ollama-cpu:11434"))
    }
    return status

def display_error(message: str) -> None:
    """
    Display an error message in Streamlit
    """
    st.error(f"⚠️ {message}")

def display_success(message: str) -> None:
    """
    Display a success message in Streamlit
    """
    st.success(f"✅ {message}")

def display_info(message: str) -> None:
    """
    Display an info message in Streamlit
    """
    st.info(f"ℹ️ {message}")

def display_warning(message: str) -> None:
    """
    Display a warning message in Streamlit
    """
    st.warning(f"⚠️ {message}")

def get_model_info(model_name: str) -> dict:
    """
    Get information about a specific model
    """
    models = {
        "gpt-4-turbo-preview": {
            "name": "GPT-4 Turbo",
            "provider": "openai",
            "requires_key": True,
            "description": "Latest GPT-4 model with improved performance and lower latency"
        },
        "claude-3-opus-20240229": {
            "name": "Claude 3 Opus",
            "provider": "anthropic",
            "requires_key": True,
            "description": "Most capable Claude model, ideal for complex tasks"
        },
        "qwen2.5-coder:7b": {
            "name": "Qwen 2.5 Coder 7B",
            "provider": "ollama",
            "requires_key": False,
            "description": "Optimized for code generation and technical tasks"
        },
        "llama2-uncensored:7b": {
            "name": "Llama 2 Uncensored 7B",
            "provider": "ollama",
            "requires_key": False,
            "description": "Uncensored version of Meta's Llama 2 model"
        },
        "dolphin-mistral:7b": {
            "name": "Dolphin Mistral 7B",
            "provider": "ollama",
            "requires_key": False,
            "description": "Fine-tuned Mistral model with improved capabilities"
        }
    }
    return models.get(model_name, {
        "name": model_name,
        "provider": "unknown",
        "requires_key": False,
        "description": "Custom model"
    })

def format_code(code: str, language: str = "python") -> str:
    """
    Format code for display in Streamlit
    """
    return f"```{language}\n{code}\n```"

def get_session_state(key: str, default=None):
    """
    Safely get a value from Streamlit's session state
    """
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]

def set_session_state(key: str, value) -> None:
    """
    Safely set a value in Streamlit's session state
    """
    st.session_state[key] = value 
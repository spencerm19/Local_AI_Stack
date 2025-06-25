import streamlit as st
import httpx
import os
from utils.utils import display_success, display_error, display_info, get_model_info

async def test_mcp_connection(base_url: str = "http://localhost:8200") -> bool:
    """
    Test connection to MCP server
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/health")
            return response.status_code == 200
    except Exception:
        return False

async def get_available_models(base_url: str = "http://localhost:8200") -> list:
    """
    Get list of available models from MCP server
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/v1/models")
            return response.json()["models"]
    except Exception:
        return []

async def test_model(base_url: str, model_id: str, message: str) -> str:
    """
    Test a model by sending a message
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/v1/chat/completions",
                json={
                    "messages": [{"role": "user", "content": message}],
                    "model": model_id
                }
            )
            if response.status_code == 200:
                return response.json()["content"]
            else:
                return f"Error: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def mcp_tab():
    """
    Display the MCP configuration and testing page
    """
    st.markdown("""
        # Model Context Protocol (MCP)
        
        Configure and test the Model Context Protocol server, which provides a unified interface
        for multiple language model providers.
        
        ## Server Status
    """)
    
    # MCP server configuration
    mcp_url = st.text_input(
        "MCP Server URL",
        value=os.getenv("MCP_BASE_URL", "http://localhost:8200"),
        help="The base URL for your MCP server"
    )
    
    # Test connection
    if st.button("Test Connection"):
        if asyncio.run(test_mcp_connection(mcp_url)):
            display_success("Successfully connected to MCP server")
        else:
            display_error("Failed to connect to MCP server")
    
    # Model information
    st.markdown("## Available Models")
    
    models = asyncio.run(get_available_models(mcp_url))
    if models:
        for model in models:
            with st.expander(f"{model['name']} ({model['provider'].title()})"):
                model_info = get_model_info(model["id"])
                st.markdown(f"""
                    **Provider**: {model['provider'].title()}  
                    **API Key Required**: {'Yes' if model['requires_key'] else 'No'}  
                    **Description**: {model_info['description']}
                """)
    else:
        display_warning("No models available or couldn't fetch model list")
    
    # Model testing
    st.markdown("## Model Testing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        test_model_id = st.selectbox(
            "Select Model",
            options=[m["id"] for m in models] if models else [],
            help="Choose a model to test"
        )
    
    with col2:
        test_message = st.text_input(
            "Test Message",
            value="Hello! Can you help me test if you're working correctly?",
            help="Enter a message to send to the model"
        )
    
    if st.button("Test Model") and test_model_id:
        with st.spinner("Testing model..."):
            response = asyncio.run(test_model(mcp_url, test_model_id, test_message))
            if response.startswith("Error:"):
                display_error(response)
            else:
                st.markdown("### Response")
                st.markdown(response)
    
    # Configuration help
    with st.expander("Need Help?"):
        st.markdown("""
            ### MCP Configuration Guide
            
            The Model Context Protocol (MCP) server provides a unified interface for multiple language model providers:
            
            1. **OpenAI Models**
               - Requires API key in environment
               - Supports latest GPT-4 and GPT-3.5 models
            
            2. **Anthropic Models**
               - Requires API key in environment
               - Supports Claude 3 models
            
            3. **Ollama Models**
               - No API key required
               - Runs models locally
               - Includes Qwen, Llama 2, and more
            
            ### Troubleshooting
            
            1. **Connection Issues**
               - Verify the MCP server is running
               - Check the URL is correct
               - Ensure network connectivity
            
            2. **Model Errors**
               - Verify API keys are configured
               - Check model availability
               - Review error messages
            
            3. **Performance Issues**
               - Consider using local models for faster response
               - Check system resources
               - Monitor network latency
            
            For more detailed information, check the documentation or contact support.
        """) 
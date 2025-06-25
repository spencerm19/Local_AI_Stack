import streamlit as st
import os
from dotenv import load_dotenv, set_key
from utils.utils import display_success, display_error, display_info, check_environment

def save_env_var(key: str, value: str) -> None:
    """
    Save an environment variable to the .env file
    """
    try:
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        if not os.path.exists(env_path):
            with open(env_path, 'w') as f:
                f.write('')
        
        set_key(env_path, key, value)
        os.environ[key] = value
        display_success(f"Successfully saved {key}")
    except Exception as e:
        display_error(f"Error saving {key}: {str(e)}")

def environment_tab():
    """
    Display the environment configuration page
    """
    st.markdown("""
        # Environment Configuration
        
        Configure your API keys and connection settings for various services.
        These settings will be saved in your `.env` file.
        
        ## Model Providers
    """)
    
    # OpenAI Configuration
    st.markdown("### OpenAI")
    openai_key = st.text_input(
        "OpenAI API Key",
        value=os.getenv("OPENAI_API_KEY", ""),
        type="password",
        help="Your OpenAI API key from https://platform.openai.com/account/api-keys"
    )
    if st.button("Save OpenAI Key"):
        save_env_var("OPENAI_API_KEY", openai_key)
    
    # Anthropic Configuration
    st.markdown("### Anthropic")
    anthropic_key = st.text_input(
        "Anthropic API Key",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        type="password",
        help="Your Anthropic API key from https://console.anthropic.com/account/keys"
    )
    if st.button("Save Anthropic Key"):
        save_env_var("ANTHROPIC_API_KEY", anthropic_key)
    
    # Ollama Configuration
    st.markdown("### Ollama")
    ollama_url = st.text_input(
        "Ollama Base URL",
        value=os.getenv("OLLAMA_BASE_URL", "http://ollama-cpu:11434"),
        help="The base URL for your Ollama instance"
    )
    if st.button("Save Ollama URL"):
        save_env_var("OLLAMA_BASE_URL", ollama_url)
    
    st.markdown("## Infrastructure")
    
    # Supabase Configuration
    st.markdown("### Supabase")
    supabase_url = st.text_input(
        "Supabase URL",
        value=os.getenv("SUPABASE_URL", ""),
        help="Your Supabase project URL"
    )
    supabase_key = st.text_input(
        "Supabase Key",
        value=os.getenv("SUPABASE_KEY", ""),
        type="password",
        help="Your Supabase project API key"
    )
    if st.button("Save Supabase Configuration"):
        save_env_var("SUPABASE_URL", supabase_url)
        save_env_var("SUPABASE_KEY", supabase_key)
    
    # Environment Status
    st.markdown("## Current Status")
    status = check_environment()
    
    # Display status in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Model Providers")
        if status["openai"]:
            st.success("✅ OpenAI API Connected")
        else:
            st.warning("⚠️ OpenAI API Not Configured")
            
        if status["anthropic"]:
            st.success("✅ Anthropic API Connected")
        else:
            st.warning("⚠️ Anthropic API Not Configured")
            
        if status["ollama"]:
            st.success("✅ Ollama Connected")
        else:
            st.warning("⚠️ Ollama Not Connected")
    
    with col2:
        st.markdown("### Infrastructure")
        if status["supabase"]:
            st.success("✅ Supabase Connected")
        else:
            st.warning("⚠️ Supabase Not Configured")
    
    # Environment Variables
    if st.checkbox("Show All Environment Variables"):
        st.markdown("### All Environment Variables")
        env_vars = {
            key: value if not any(secret in key.lower() for secret in ["key", "password", "secret", "token"]) 
            else "********"
            for key, value in os.environ.items()
        }
        st.json(env_vars)
    
    # Help Section
    with st.expander("Need Help?"):
        st.markdown("""
            ### Troubleshooting Tips
            
            1. **API Keys Not Working?**
               - Double-check that you've copied the entire key
               - Ensure there are no extra spaces
               - Verify the key is active in your provider's dashboard
            
            2. **Supabase Connection Issues?**
               - Confirm your project is running
               - Check the URL format (should start with https://)
               - Verify you're using the correct API key type (anon or service_role)
            
            3. **Ollama Connection Issues?**
               - Ensure Ollama is running in your Local AI Stack
               - Check if the port is correctly exposed (default: 11434)
               - Verify network connectivity between services
            
            ### Documentation Links
            
            - [OpenAI API Documentation](https://platform.openai.com/docs)
            - [Anthropic API Documentation](https://docs.anthropic.com)
            - [Supabase Documentation](https://supabase.com/docs)
            - [Ollama Documentation](https://ollama.ai/docs)
        """) 
import streamlit as st
from utils.utils import display_info, get_model_info, check_environment

def intro_tab():
    """
    Display the introduction page
    """
    # Welcome section
    st.markdown("""
        # Welcome to Archon AI Stack! 🤖
        
        Archon AI Stack is a comprehensive development environment that combines the power of Local AI Stack 
        with Archon's agent-building capabilities. This integrated platform provides you with all the tools 
        you need to build, test, and deploy AI agents.
        
        ## Core Features
        
        ### 🔧 Local AI Stack Integration
        - **Ollama**: Run powerful language models locally
        - **n8n**: Create automated workflows
        - **Supabase**: Store and manage your data
        - **Qdrant**: Vector database for embeddings
        - **Flowise**: Visual flow programming
        - **Open WebUI**: User-friendly interface
        
        ### 🤖 Archon Agent Builder
        - Build custom AI agents with a visual interface
        - Test and iterate on agent behavior
        - Deploy agents to production
        - Monitor agent performance
        
        ### 🔌 Model Context Protocol (MCP)
        - Unified interface for multiple LLM providers
        - Seamless model switching
        - Consistent API across providers
        
        ## Environment Status
    """)
    
    # Check environment status
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
    
    # Available models section
    st.markdown("## Available Models")
    
    # Create a card for each model
    for model_id in ["gpt-4-turbo-preview", "claude-3-opus-20240229", "qwen2.5-coder:7b", "llama2-uncensored:7b", "dolphin-mistral:7b"]:
        model = get_model_info(model_id)
        with st.expander(f"{model['name']} ({model['provider'].title()})"):
            st.markdown(f"""
                **Provider**: {model['provider'].title()}  
                **API Key Required**: {'Yes' if model['requires_key'] else 'No'}  
                **Description**: {model['description']}
            """)
    
    # Getting started section
    st.markdown("""
        ## Getting Started
        
        1. **Configure Environment**: Set up your API keys and connections in the Environment tab
        2. **Test Database**: Verify your database connection in the Database tab
        3. **Build an Agent**: Start creating your agent in the Chat tab
        4. **Monitor & Deploy**: Use the Agent Service tab to manage your agents
        
        ## Need Help?
        
        - Check the Documentation tab for detailed guides
        - Visit our GitHub repository for the latest updates
        - Join our community for support and discussions
    """)
    
    # Display version information
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        **Version**: 1.0.0  
        **Build**: 2024.03.01
    """) 
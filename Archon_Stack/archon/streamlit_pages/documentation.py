import streamlit as st
from typing import Optional
from supabase import Client
from utils.utils import display_info

def documentation_tab(supabase: Optional[Client]):
    """
    Display the documentation page
    """
    st.markdown("""
        # Documentation
        
        Welcome to the Archon AI Stack documentation. This guide will help you understand
        and effectively use all features of the platform.
        
        ## Core Components
        
        ### Local AI Stack
        
        The Local AI Stack provides the foundation for running AI models and services locally:
        
        - **Ollama**: Run open-source language models locally
        - **n8n**: Create automated workflows
        - **Supabase**: Database and authentication
        - **Qdrant**: Vector database for embeddings
        - **Flowise**: Visual AI development
        - **Open WebUI**: User interface for local models
        
        ### Archon Agent Builder
        
        The Agent Builder allows you to create and manage AI agents:
        
        - Create custom agents with specific behaviors
        - Test and iterate on agent responses
        - Deploy agents to production
        - Monitor agent performance
        
        ### Model Context Protocol (MCP)
        
        MCP provides a unified interface for multiple LLM providers:
        
        - Switch between different models seamlessly
        - Consistent API across providers
        - Support for both local and cloud models
        
        ## Getting Started
        
        1. **Environment Setup**
           - Configure API keys in the Environment tab
           - Test database connection
           - Verify model availability
        
        2. **Creating Your First Agent**
           - Navigate to the Chat tab
           - Define agent behavior
           - Test responses
           - Save successful configurations
        
        3. **Managing Agents**
           - Use the Agent Service tab
           - Monitor performance
           - Update configurations
           - View conversation history
        
        4. **Using MCP**
           - Configure MCP server
           - Test available models
           - Switch between providers
        
        ## Best Practices
        
        1. **Agent Development**
           - Start with clear objectives
           - Test thoroughly
           - Iterate based on feedback
           - Document configurations
        
        2. **Model Selection**
           - Choose appropriate models for tasks
           - Consider cost vs. performance
           - Test with different parameters
        
        3. **Data Management**
           - Regular database backups
           - Monitor storage usage
           - Clean up unused data
        
        4. **Security**
           - Secure API keys
           - Regular access reviews
           - Monitor usage patterns
        
        ## Troubleshooting
        
        If you encounter issues:
        
        1. Check the Environment tab for configuration
        2. Verify service connectivity
        3. Review error messages
        4. Check system resources
        
        For additional support, visit our GitHub repository or contact the support team.
    """)
    
    # Display version information
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        **Documentation Version**: 1.0.0  
        **Last Updated**: 2024.03.01
    """) 
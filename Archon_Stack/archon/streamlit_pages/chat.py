import streamlit as st
import httpx
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from utils.utils import display_success, display_error, display_info, get_model_info, get_session_state, set_session_state

async def send_message(message: str, model: str, conversation_history: List[Dict[str, str]], base_url: str = "http://localhost:8200") -> str:
    """
    Send a message to the MCP server and get a response
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/v1/chat/completions",
                json={
                    "messages": conversation_history + [{"role": "user", "content": message}],
                    "model": model
                }
            )
            if response.status_code == 200:
                return response.json()["content"]
            else:
                return f"Error: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def save_conversation(supabase, agent_id: str, title: str, messages: List[Dict[str, str]], metadata: Dict[str, Any]) -> None:
    """
    Save conversation to Supabase
    """
    try:
        conversation_id = str(uuid.uuid4())
        supabase.table("conversations").insert({
            "id": conversation_id,
            "agent_id": agent_id,
            "title": title,
            "messages": messages,
            "metadata": metadata,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }).execute()
        display_success("Conversation saved successfully")
    except Exception as e:
        display_error(f"Error saving conversation: {str(e)}")

def load_conversation(supabase, conversation_id: str) -> Optional[Dict[str, Any]]:
    """
    Load conversation from Supabase
    """
    try:
        result = supabase.table("conversations").select("*").eq("id", conversation_id).execute()
        if result.data:
            return result.data[0]
        return None
    except Exception as e:
        display_error(f"Error loading conversation: {str(e)}")
        return None

async def chat_tab():
    """
    Display the agent builder chat interface
    """
    st.markdown("""
        # Agent Builder Chat
        
        Build and test AI agents through natural conversation.
        The chat interface allows you to interact with different models and save agent configurations.
    """)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_agent_id" not in st.session_state:
        st.session_state.current_agent_id = str(uuid.uuid4())
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### Chat Configuration")
        
        # Model selection
        available_models = await get_available_models()
        model = st.selectbox(
            "Select Model",
            options=[m["id"] for m in available_models] if available_models else ["gpt-4-turbo-preview"],
            help="Choose the model to chat with"
        )
        
        # Save conversation
        if st.button("Save Conversation"):
            title = st.text_input("Conversation Title", value=f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            metadata = {
                "model": model,
                "timestamp": datetime.utcnow().isoformat()
            }
            save_conversation(
                st.session_state.get("supabase"),
                st.session_state.current_agent_id,
                title,
                st.session_state.messages,
                metadata
            )
        
        # Load conversation
        if st.session_state.get("supabase"):
            conversations = st.session_state.supabase.table("conversations").select("id", "title").execute()
            if conversations.data:
                selected_conversation = st.selectbox(
                    "Load Conversation",
                    options=[(c["id"], c["title"]) for c in conversations.data],
                    format_func=lambda x: x[1]
                )
                if st.button("Load"):
                    conversation = load_conversation(st.session_state.supabase, selected_conversation[0])
                    if conversation:
                        st.session_state.messages = conversation["messages"]
                        st.session_state.current_agent_id = conversation["agent_id"]
                        st.experimental_rerun()
        
        # Clear chat
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.experimental_rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = await send_message(prompt, model, st.session_state.messages[:-1])
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Help section
    with st.expander("Need Help?"):
        st.markdown("""
            ### Chat Interface Guide
            
            1. **Model Selection**
               - Choose from available models in the sidebar
               - Each model has different capabilities and costs
            
            2. **Conversation Management**
               - Save conversations to continue later
               - Load previous conversations
               - Clear chat to start fresh
            
            3. **Best Practices**
               - Be specific in your requests
               - Provide context when needed
               - Use system messages for consistent behavior
            
            4. **Agent Building Tips**
               - Start with a clear goal
               - Test different approaches
               - Iterate based on responses
               - Save successful configurations
            
            For more detailed information, check the documentation.
        """) 
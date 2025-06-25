import streamlit as st
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from utils.utils import display_success, display_error, display_info, get_model_info

def create_agent(supabase, name: str, description: str, configuration: Dict[str, Any]) -> str:
    """
    Create a new agent in Supabase
    """
    try:
        agent_id = str(uuid.uuid4())
        supabase.table("agents").insert({
            "id": agent_id,
            "name": name,
            "description": description,
            "configuration": configuration,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }).execute()
        return agent_id
    except Exception as e:
        raise Exception(f"Error creating agent: {str(e)}")

def update_agent(supabase, agent_id: str, name: str, description: str, configuration: Dict[str, Any]) -> None:
    """
    Update an existing agent in Supabase
    """
    try:
        supabase.table("agents").update({
            "name": name,
            "description": description,
            "configuration": configuration,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", agent_id).execute()
    except Exception as e:
        raise Exception(f"Error updating agent: {str(e)}")

def delete_agent(supabase, agent_id: str) -> None:
    """
    Delete an agent from Supabase
    """
    try:
        # Delete associated conversations first
        supabase.table("conversations").delete().eq("agent_id", agent_id).execute()
        # Then delete the agent
        supabase.table("agents").delete().eq("id", agent_id).execute()
    except Exception as e:
        raise Exception(f"Error deleting agent: {str(e)}")

def get_agent(supabase, agent_id: str) -> Optional[Dict[str, Any]]:
    """
    Get agent details from Supabase
    """
    try:
        result = supabase.table("agents").select("*").eq("id", agent_id).execute()
        if result.data:
            return result.data[0]
        return None
    except Exception as e:
        raise Exception(f"Error getting agent: {str(e)}")

def get_agent_conversations(supabase, agent_id: str) -> List[Dict[str, Any]]:
    """
    Get conversations for an agent from Supabase
    """
    try:
        result = supabase.table("conversations").select("*").eq("agent_id", agent_id).execute()
        return result.data
    except Exception as e:
        raise Exception(f"Error getting conversations: {str(e)}")

def agent_service_tab():
    """
    Display the agent service management interface
    """
    st.markdown("""
        # Agent Service
        
        Manage your AI agents and monitor their performance.
        Create, update, and delete agents, and view their conversation history.
    """)
    
    # Check if Supabase is configured
    if not st.session_state.get("supabase"):
        display_error("Supabase client not initialized. Please configure your Supabase credentials in the Environment tab.")
        return
    
    # Sidebar actions
    with st.sidebar:
        st.markdown("### Agent Actions")
        action = st.radio(
            "Select Action",
            ["Create Agent", "View/Edit Agent", "Delete Agent"]
        )
    
    if action == "Create Agent":
        st.markdown("## Create New Agent")
        
        # Basic information
        name = st.text_input("Agent Name", help="A unique name for your agent")
        description = st.text_area("Description", help="Describe what this agent does")
        
        # Model configuration
        st.markdown("### Model Configuration")
        model = st.selectbox(
            "Default Model",
            options=["gpt-4-turbo-preview", "claude-3-opus-20240229", "qwen2.5-coder:7b"],
            help="Choose the default model for this agent"
        )
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            help="Control randomness in responses"
        )
        
        # System message
        system_message = st.text_area(
            "System Message",
            help="Set the agent's behavior and role",
            value="You are a helpful AI assistant."
        )
        
        # Create agent button
        if st.button("Create Agent"):
            try:
                configuration = {
                    "model": model,
                    "temperature": temperature,
                    "system_message": system_message
                }
                agent_id = create_agent(
                    st.session_state.supabase,
                    name,
                    description,
                    configuration
                )
                display_success(f"Agent created successfully with ID: {agent_id}")
            except Exception as e:
                display_error(str(e))
    
    elif action == "View/Edit Agent":
        st.markdown("## View/Edit Agent")
        
        # Get all agents
        agents = st.session_state.supabase.table("agents").select("*").execute()
        if not agents.data:
            display_info("No agents found. Create one first!")
            return
        
        # Select agent
        selected_agent = st.selectbox(
            "Select Agent",
            options=[(a["id"], a["name"]) for a in agents.data],
            format_func=lambda x: x[1]
        )
        
        if selected_agent:
            agent = get_agent(st.session_state.supabase, selected_agent[0])
            if agent:
                # Edit form
                st.markdown("### Edit Agent")
                
                name = st.text_input("Agent Name", value=agent["name"])
                description = st.text_area("Description", value=agent["description"])
                
                st.markdown("### Model Configuration")
                model = st.selectbox(
                    "Default Model",
                    options=["gpt-4-turbo-preview", "claude-3-opus-20240229", "qwen2.5-coder:7b"],
                    index=["gpt-4-turbo-preview", "claude-3-opus-20240229", "qwen2.5-coder:7b"].index(agent["configuration"]["model"])
                )
                temperature = st.slider(
                    "Temperature",
                    min_value=0.0,
                    max_value=1.0,
                    value=agent["configuration"]["temperature"]
                )
                system_message = st.text_area(
                    "System Message",
                    value=agent["configuration"]["system_message"]
                )
                
                # Update button
                if st.button("Update Agent"):
                    try:
                        configuration = {
                            "model": model,
                            "temperature": temperature,
                            "system_message": system_message
                        }
                        update_agent(
                            st.session_state.supabase,
                            agent["id"],
                            name,
                            description,
                            configuration
                        )
                        display_success("Agent updated successfully")
                    except Exception as e:
                        display_error(str(e))
                
                # Conversation history
                st.markdown("### Conversation History")
                conversations = get_agent_conversations(st.session_state.supabase, agent["id"])
                if conversations:
                    for conv in conversations:
                        with st.expander(f"{conv['title']} ({conv['created_at']})"):
                            st.json(conv["messages"])
                else:
                    st.info("No conversations found for this agent")
    
    elif action == "Delete Agent":
        st.markdown("## Delete Agent")
        
        # Get all agents
        agents = st.session_state.supabase.table("agents").select("*").execute()
        if not agents.data:
            display_info("No agents found!")
            return
        
        # Select agent to delete
        selected_agent = st.selectbox(
            "Select Agent to Delete",
            options=[(a["id"], a["name"]) for a in agents.data],
            format_func=lambda x: x[1]
        )
        
        if selected_agent:
            st.warning(f"Are you sure you want to delete agent '{selected_agent[1]}'? This action cannot be undone!")
            if st.button("Delete Agent"):
                try:
                    delete_agent(st.session_state.supabase, selected_agent[0])
                    display_success("Agent deleted successfully")
                    st.experimental_rerun()
                except Exception as e:
                    display_error(str(e))
    
    # Help section
    with st.expander("Need Help?"):
        st.markdown("""
            ### Agent Management Guide
            
            1. **Creating Agents**
               - Give your agent a clear, descriptive name
               - Write a detailed description of its purpose
               - Configure the model settings carefully
               - Set an appropriate system message
            
            2. **Editing Agents**
               - Update configuration as needed
               - Monitor conversation history
               - Adjust parameters based on performance
            
            3. **Deleting Agents**
               - Backup important conversations first
               - Consider archiving instead of deleting
               - Deletion removes all associated data
            
            4. **Best Practices**
               - Test agents thoroughly before deployment
               - Document configuration changes
               - Monitor performance regularly
               - Keep system messages focused
            
            For more detailed information, check the documentation.
        """) 
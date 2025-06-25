import streamlit as st
from supabase import Client
from utils.utils import display_success, display_error, display_info
import json
from typing import Optional, List, Dict, Any

def create_tables(supabase: Client) -> None:
    """
    Create necessary tables in Supabase
    """
    try:
        # Create agents table
        supabase.table("agents").select("id").limit(1).execute()
    except:
        supabase.table("agents").create([
            {"name": "id", "type": "uuid", "primary": True},
            {"name": "name", "type": "text"},
            {"name": "description", "type": "text"},
            {"name": "configuration", "type": "jsonb"},
            {"name": "created_at", "type": "timestamp with time zone"},
            {"name": "updated_at", "type": "timestamp with time zone"}
        ])
        display_success("Created agents table")
    
    try:
        # Create conversations table
        supabase.table("conversations").select("id").limit(1).execute()
    except:
        supabase.table("conversations").create([
            {"name": "id", "type": "uuid", "primary": True},
            {"name": "agent_id", "type": "uuid"},
            {"name": "title", "type": "text"},
            {"name": "messages", "type": "jsonb"},
            {"name": "metadata", "type": "jsonb"},
            {"name": "created_at", "type": "timestamp with time zone"},
            {"name": "updated_at", "type": "timestamp with time zone"}
        ])
        display_success("Created conversations table")
    
    try:
        # Create tools table
        supabase.table("tools").select("id").limit(1).execute()
    except:
        supabase.table("tools").create([
            {"name": "id", "type": "uuid", "primary": True},
            {"name": "name", "type": "text"},
            {"name": "description", "type": "text"},
            {"name": "schema", "type": "jsonb"},
            {"name": "created_at", "type": "timestamp with time zone"},
            {"name": "updated_at", "type": "timestamp with time zone"}
        ])
        display_success("Created tools table")

def get_table_info(supabase: Client, table_name: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a table
    """
    try:
        # Get table schema
        schema = supabase.table(table_name).select("*").limit(0).execute()
        
        # Get row count
        count = supabase.table(table_name).select("*", count="exact").execute()
        
        return {
            "exists": True,
            "row_count": count.count if count else 0,
            "schema": schema.data if schema else None
        }
    except Exception as e:
        return {
            "exists": False,
            "error": str(e)
        }

def database_tab(supabase: Optional[Client]):
    """
    Display the database configuration and management page
    """
    st.markdown("""
        # Database Configuration
        
        Manage your Supabase database configuration and tables.
        This interface allows you to initialize and manage the required tables for Archon.
        
        ## Database Status
    """)
    
    if not supabase:
        display_error("Supabase client not initialized. Please configure your Supabase credentials in the Environment tab.")
        return
    
    # Database connection test
    try:
        supabase.table("agents").select("id").limit(1).execute()
        display_success("Successfully connected to Supabase")
    except Exception as e:
        display_error(f"Failed to connect to Supabase: {str(e)}")
        return
    
    # Table management
    st.markdown("## Table Management")
    
    # Initialize tables button
    if st.button("Initialize Tables"):
        try:
            create_tables(supabase)
            display_success("Successfully initialized all tables")
        except Exception as e:
            display_error(f"Error initializing tables: {str(e)}")
    
    # Table information
    st.markdown("## Table Information")
    
    tables = ["agents", "conversations", "tools"]
    for table in tables:
        with st.expander(f"{table.title()} Table"):
            info = get_table_info(supabase, table)
            if info["exists"]:
                st.markdown(f"""
                    **Status**: ✅ Exists  
                    **Row Count**: {info.get('row_count', 'N/A')}
                """)
                
                if info.get('schema'):
                    st.markdown("### Schema")
                    st.json(info['schema'])
            else:
                st.markdown(f"""
                    **Status**: ❌ Does not exist  
                    **Error**: {info.get('error', 'Unknown error')}
                """)
    
    # Database operations
    st.markdown("## Database Operations")
    
    # Export data
    if st.button("Export All Data"):
        try:
            data = {}
            for table in tables:
                result = supabase.table(table).select("*").execute()
                data[table] = result.data
            
            st.download_button(
                "Download Data (JSON)",
                data=json.dumps(data, indent=2),
                file_name="archon_data_export.json",
                mime="application/json"
            )
            display_success("Data exported successfully")
        except Exception as e:
            display_error(f"Error exporting data: {str(e)}")
    
    # Import data
    uploaded_file = st.file_uploader("Import Data (JSON)", type="json")
    if uploaded_file and st.button("Import Data"):
        try:
            data = json.loads(uploaded_file.getvalue())
            for table, rows in data.items():
                if rows:
                    supabase.table(table).upsert(rows).execute()
            display_success("Data imported successfully")
        except Exception as e:
            display_error(f"Error importing data: {str(e)}")
    
    # Help section
    with st.expander("Need Help?"):
        st.markdown("""
            ### Database Management Tips
            
            1. **First Time Setup**
               - Click "Initialize Tables" to create the required tables
               - This will not affect existing tables
            
            2. **Data Backup**
               - Use the "Export All Data" button regularly
               - Keep the JSON file in a safe location
            
            3. **Data Recovery**
               - Use the "Import Data" function to restore from a backup
               - The import will update existing records and add new ones
            
            4. **Troubleshooting**
               - If tables are missing, try initializing them again
               - Check the Supabase dashboard for detailed logs
               - Ensure your database permissions are correctly set
            
            ### Table Descriptions
            
            - **Agents**: Stores agent configurations and metadata
            - **Conversations**: Records chat history and interactions
            - **Tools**: Maintains the tool library available to agents
            
            For more detailed information, check the documentation or contact support.
        """) 
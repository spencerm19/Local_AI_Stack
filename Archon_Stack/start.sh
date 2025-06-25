#!/bin/bash

# Check if .env file exists, if not create from template
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp env.template .env
    echo "Please edit .env file with your settings before continuing."
    exit 1
fi

# Function to wait for a service to be ready
wait_for_service() {
    local service=$1
    local port=$2
    echo "Waiting for $service to be ready..."
    while ! nc -z localhost $port; do
        sleep 1
    done
    echo "$service is ready!"
}

# Pull required Ollama models
pull_ollama_models() {
    echo "Pulling Ollama models..."
    models=$(grep OLLAMA_MODELS .env | cut -d '=' -f2 | tr ',' ' ')
    for model in $models; do
        docker exec ollama-cpu ollama pull $model
    done
}

# Start services
echo "Starting services in CPU mode..."

# Start core services
docker-compose up -d

# Wait for key services
wait_for_service "Supabase" 5432
wait_for_service "Ollama" 11434
wait_for_service "Qdrant" 6333
wait_for_service "Neo4j" 7474
wait_for_service "SearXNG" 8080
wait_for_service "Langfuse" 3003

# Pull Ollama models
pull_ollama_models

# Initialize database schema if needed
echo "Initializing database schema..."
docker exec archon python -c "from streamlit_pages.database import initialize_database; initialize_database()"

echo "All services are up and running!"
echo "Access the services at:"
echo "- Archon UI: http://localhost:8501"
echo "- n8n: http://localhost:5678"
echo "- Flowise: http://localhost:3001"
echo "- Open WebUI: http://localhost:3000"
echo "- Qdrant: http://localhost:6333"
echo "- MCP Crawl4AI: http://localhost:3002"
echo "- Neo4j Browser: http://localhost:7474"
echo "- SearXNG: http://localhost:8080"
echo "- Langfuse: http://localhost:3003" 

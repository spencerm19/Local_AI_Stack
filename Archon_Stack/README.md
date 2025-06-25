# Archon AI Stack

A comprehensive AI development environment that combines the power of Local AI Stack with Archon's agent-building capabilities and advanced RAG capabilities through MCP Crawl4AI. This project integrates multiple AI tools and services into a unified, containerized environment.

## Core Components

### Archon Agent Builder
- **Agent Generation**: Create custom AI agents using advanced agentic coding workflow
- **Multi-Agent System**: Planning and execution separation with LangGraph
- **MCP Integration**: Seamless integration with AI IDEs
- **Streamlit UI**: Comprehensive interface for managing all aspects

### Local AI Stack Services
- **Ollama**: Local LLM serving with support for various models
- **n8n**: Workflow automation and integration
- **Supabase**: Database and storage backend
- **Qdrant**: Vector database for embeddings
- **Flowise**: Flow-based programming interface
- **Open WebUI**: User interface for Ollama

### MCP Crawl4AI Integration
- **Web Crawling**: Advanced web crawling capabilities
- **RAG Pipeline**: Sophisticated retrieval-augmented generation
- **MCP Protocol**: Standardized interface for AI tools

## Prerequisites

- Docker and Docker Compose
- PowerShell 7+ (for Windows users)
- For GPU support:
  - NVIDIA: NVIDIA Docker runtime and appropriate drivers
  - AMD: ROCm support and appropriate drivers

## Quick Start

1. Clone this repository:
```bash
git clone <your-repo-url>
cd archon_stack
```

2. Configure your environment:
```bash
# Copy the environment template
cp env.template .env

# Edit the .env file with your settings
nano .env  # or use your preferred editor
```

3. Start the services:

For CPU-only mode:
```bash
./start.sh cpu
```

For NVIDIA GPU support:
```bash
./start.sh gpu-nvidia
```

For AMD GPU support:
```bash
./start.sh gpu-amd
```

## Available Services

After starting, the following services will be available:

| Service      | URL                     | Default Port |
|--------------|-------------------------|--------------|
| Archon UI    | http://localhost:8501   | 8501        |
| n8n          | http://localhost:5678   | 5678        |
| Open WebUI   | http://localhost:3000   | 3000        |
| Flowise      | http://localhost:3001   | 3001        |
| MCP Crawl4AI | http://localhost:3002   | 3002        |
| Qdrant       | http://localhost:6333   | 6333        |
| Ollama       | http://localhost:11434  | 11434       |

## Environment Configuration

Key environment variables in `.env`:

### Core Settings
- `SERVER_IP`: Host IP address
- `OPENAI_API_KEY`: OpenAI API key (optional)
- `ANTHROPIC_API_KEY`: Anthropic API key (optional)

### Database
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user

### n8n
- `N8N_ENCRYPTION_KEY`: Encryption key
- `N8N_JWT_SECRET`: JWT secret

### Flowise
- `FLOWISE_USERNAME`: Admin username
- `FLOWISE_PASSWORD`: Admin password
- `FLOWISE_SECRET_KEY`: Secret key

### Archon
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase API key
- `ARCHON_PORT`: UI port (default: 8501)
- `ARCHON_SERVICE_PORT`: Service port (default: 8100)

### Ollama
- `OLLAMA_MODELS`: Comma-separated list of models to pull
- `OLLAMA_PORT`: API port (default: 11434)

## GPU Support

The system supports both NVIDIA and AMD GPUs:

### NVIDIA Setup
- Requires NVIDIA Docker runtime
- Automatically installs NVIDIA Container Toolkit
- Uses NVIDIA GPU for compatible models

### AMD Setup
- Requires ROCm support
- Automatically installs ROCm OpenCL development package
- Uses AMD GPU for compatible models

## Managing Services

### Basic Commands
- View logs: `docker-compose logs -f [service_name]`
- Stop services: `docker-compose down`
- Restart services: Run the start script again
- Update services: `docker-compose pull`

### Data Persistence

All data is persisted in Docker volumes:

- `archon_data`: Archon workbench data
- `ollama_storage`: Ollama models
- `n8n_storage`: n8n workflows and data
- `flowise_storage`: Flowise configurations
- `qdrant_storage`: Vector database data
- `supabase_db_data`: PostgreSQL database
- `supabase_storage_data`: File storage

## Security Notes

1. Always change default passwords in the `.env` file
2. Use strong encryption keys and JWT secrets
3. Consider enabling authentication for services in production
4. Review and adjust port exposures based on your needs
5. Secure your API keys and credentials

## Troubleshooting

### Common Issues

1. Service startup failures:
   - Check Docker logs: `docker-compose logs [service_name]`
   - Verify port availability
   - Check GPU driver compatibility

2. Database connection issues:
   - Verify PostgreSQL password in `.env`
   - Check if database service is running
   - Ensure no port conflicts

3. GPU-related problems:
   - Verify driver installation
   - Check Docker GPU runtime configuration
   - Confirm hardware compatibility

4. Archon agent generation issues:
   - Check Supabase connection
   - Verify LLM API keys if using cloud models
   - Check Ollama connection for local models

## Contributing

Contributions are welcome! Please feel free to:
- Submit pull requests
- Report bugs
- Suggest new features
- Share your agent templates
- Contribute to the tool library

## License

This project combines several open-source projects, each with their own licenses. Please refer to the individual repositories for their specific licenses. 
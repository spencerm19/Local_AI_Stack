# Local_AI_Stack

This project combines several powerful AI and development tools into a single, easy-to-use Docker environment. It integrates:

- Ollama (AI model serving)
- n8n (Workflow automation)
- Supabase (Database and storage)
- Qdrant (Vector database)
- Flowise (Flow-based programming)
- Open WebUI (UI for Ollama)

## Prerequisites

- Docker and Docker Compose
- PowerShell 7+ (for Windows users)
- NVIDIA Docker runtime (for GPU support with NVIDIA cards)
- ROCm support (for GPU support with AMD cards)

## Quick Start

1. Clone this repository:
```powershell
git clone <your-repo-url>
cd freya_ai
```

2. Copy the example environment file and configure it:
```powershell
Copy-Item .env.example .env
```
Edit the `.env` file and set your desired configuration values.

3. Start the services:

For CPU-only mode:
```powershell
./start.ps1 -Profile cpu
```

For NVIDIA GPU support:
```powershell
./start.ps1 -Profile gpu-nvidia
```

For AMD GPU support:
```powershell
./start.ps1 -Profile gpu-amd
```

## Available Services

After starting, the following services will be available:

- n8n: http://localhost:5678
- Open WebUI: http://localhost:3000
- Flowise: http://localhost:3001
- Qdrant: http://localhost:6333
- Supabase PostgreSQL: localhost:5432

## Environment Variables

Key environment variables in `.env`:

- `POSTGRES_PASSWORD`: Password for PostgreSQL database
- `N8N_ENCRYPTION_KEY`: Encryption key for n8n
- `N8N_JWT_SECRET`: JWT secret for n8n
- `STORAGE_REGION`: Region for S3-compatible storage
- `STORAGE_S3_BUCKET`: Bucket name for S3-compatible storage

## GPU Support

The system supports both NVIDIA and AMD GPUs:

- NVIDIA: Requires NVIDIA Docker runtime and appropriate drivers
- AMD: Requires ROCm support and appropriate drivers

## Managing Services

- View logs: `docker compose logs -f`
- Stop services: `docker compose down`
- Restart services: Run the start script again
- Update services: Pull new images with `docker compose pull`

## Data Persistence

All data is persisted in Docker volumes:

- `n8n_storage`: n8n workflows and data
- `ollama_storage`: Ollama models
- `qdrant_storage`: Vector database data
- `supabase_db_data`: PostgreSQL database
- `supabase_storage_data`: File storage
- Other volumes for various services

## Security Notes

1. Always change default passwords in the `.env` file
2. Use strong encryption keys and JWT secrets
3. Consider enabling authentication for services in production
4. Review and adjust port exposures based on your needs

## Troubleshooting

1. If services fail to start, check:
   - Docker logs for specific services
   - Port conflicts with existing services
   - GPU driver compatibility (for GPU modes)

2. For database connection issues:
   - Verify PostgreSQL password in `.env`
   - Check if database service is running
   - Ensure no port conflicts on 5432

3. For GPU-related issues:
   - Verify driver installation
   - Check Docker GPU runtime configuration
   - Confirm hardware compatibility

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project combines several open-source projects, each with their own licenses. Please refer to the individual repositories for their specific licenses. 
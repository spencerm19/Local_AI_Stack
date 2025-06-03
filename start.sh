#!/bin/bash

# Default to CPU profile if not specified
PROFILE=${1:-cpu}

# Validate profile
if [[ ! "$PROFILE" =~ ^(cpu|gpu-nvidia|gpu-amd)$ ]]; then
    echo "Error: Invalid profile. Use one of: cpu, gpu-nvidia, gpu-amd"
    exit 1
fi

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root or with sudo"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install dependencies if needed
echo "Checking and installing dependencies..."
if ! command_exists docker; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl enable docker
    systemctl start docker
fi

if ! command_exists docker-compose; then
    echo "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create one from the .env.example template."
    exit 1
fi

# Source the .env file to get SERVER_IP
if [ -f .env ]; then
    source .env
fi

# Configure system for GPU if needed
if [ "$PROFILE" = "gpu-nvidia" ]; then
    echo "Setting up NVIDIA Docker runtime..."
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list
    apt-get update && apt-get install -y nvidia-container-toolkit
    systemctl restart docker
elif [ "$PROFILE" = "gpu-amd" ]; then
    echo "Setting up ROCm..."
    apt-get update && apt-get install -y rocm-opencl-dev
fi

# Stop any running containers
echo "Stopping any running containers..."
docker-compose down

# Start services with selected profile
echo "Starting services with $PROFILE profile..."
docker-compose --profile $PROFILE up -d

echo "Services are starting up. You can access them at:"
echo "- n8n: http://localhost:${N8N_PORT}"
echo "- Open WebUI: http://localhost:${WEBUI_PORT}"
echo "- Flowise: http://localhost:${FLOWISE_PORT}"
echo "- Qdrant: http://localhost:${QDRANT_PORT}"
echo "- Ollama: http://localhost:${OLLAMA_PORT}"

echo -e "\nAlternatively, you can access services using the host IP (${SERVER_IP}):"
echo "- n8n: http://${SERVER_IP}:${N8N_PORT}"
echo "- Open WebUI: http://${SERVER_IP}:${WEBUI_PORT}"
echo "- Flowise: http://${SERVER_IP}:${FLOWISE_PORT}"
echo "- Qdrant: http://${SERVER_IP}:${QDRANT_PORT}"
echo "- Ollama: http://${SERVER_IP}:${OLLAMA_PORT}"

echo -e "\nTo view logs, use: docker-compose logs -f"
echo "To stop services, use: docker-compose down"

# Check if services are running
echo -e "\nChecking service status..."
sleep 10
docker-compose ps 
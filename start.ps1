param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('cpu', 'gpu-nvidia', 'gpu-amd')]
    [string]$Profile = 'cpu'
)

# Function to check if Docker is running
function Test-DockerRunning {
    try {
        $dockerStatus = docker info 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
        return $false
    }
    catch {
        return $false
    }
}

# Function to check if a command exists
function Test-CommandExists {
    param (
        [string]$Command
    )
    return [bool](Get-Command -Name $Command -ErrorAction SilentlyContinue)
}

# Check if Docker is installed
if (-not (Test-CommandExists "docker")) {
    Write-Error "Docker is not installed. Please install Docker Desktop for Windows first."
    exit 1
}

# Check if Docker is running
if (-not (Test-DockerRunning)) {
    Write-Error "Docker is not running. Please start Docker Desktop and try again."
    exit 1
}

# Create .env file if it doesn't exist
if (-not (Test-Path .env)) {
    Write-Host "Creating .env file from template..."
    Copy-Item "env template" .env
    Write-Host "Please edit the .env file to set your secure passwords and keys before continuing."
    Write-Host "Press any key to continue once you've updated the .env file..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Stop any running containers
Write-Host "Stopping any running containers..."
docker compose down

# Start services with selected profile
Write-Host "Starting services with $Profile profile..."
$env:COMPOSE_PROFILES = $Profile
docker compose up -d

# Function to wait for service availability
function Wait-ForService {
    param (
        [string]$ServiceName,
        [string]$Url,
        [int]$Port,
        [int]$TimeoutSeconds = 180
    )
    
    Write-Host "Waiting for $ServiceName to be ready..." -NoNewline
    $start = Get-Date
    $ready = $false
    
    while (-not $ready -and ((Get-Date) - $start).TotalSeconds -lt $TimeoutSeconds) {
        try {
            $tcp = New-Object System.Net.Sockets.TcpClient
            $result = $tcp.BeginConnect("localhost", $Port, $null, $null)
            $ready = $result.AsyncWaitHandle.WaitOne(1000)
            $tcp.Close()
            if ($ready) {
                Write-Host " Ready!" -ForegroundColor Green
                return $true
            }
        }
        catch {
            # Ignore errors and continue waiting
        }
        Write-Host "." -NoNewline
        Start-Sleep -Seconds 2
    }
    
    if (-not $ready) {
        Write-Host " Timed out!" -ForegroundColor Red
        return $false
    }
}

# Wait for services to be ready
$services = @(
    @{Name="n8n"; Port=$env:N8N_PORT ?? 5678},
    @{Name="Open WebUI"; Port=$env:WEBUI_PORT ?? 3000},
    @{Name="Flowise"; Port=$env:FLOWISE_PORT ?? 3001},
    @{Name="Qdrant"; Port=$env:QDRANT_PORT ?? 6333},
    @{Name="Ollama"; Port=$env:OLLAMA_PORT ?? 11434}
)

foreach ($service in $services) {
    Wait-ForService -ServiceName $service.Name -Port $service.Port
}

Write-Host "`nServices are available at:"
Write-Host "- n8n: http://localhost:$($env:N8N_PORT ?? 5678)"
Write-Host "- Open WebUI: http://localhost:$($env:WEBUI_PORT ?? 3000)"
Write-Host "- Flowise: http://localhost:$($env:FLOWISE_PORT ?? 3001)"
Write-Host "- Qdrant: http://localhost:$($env:QDRANT_PORT ?? 6333)"
Write-Host "- Ollama: http://localhost:$($env:OLLAMA_PORT ?? 11434)"

Write-Host "`nImportant Notes:" -ForegroundColor Cyan
Write-Host "- Initial startup may take time as Docker images are pulled"
Write-Host "- Ollama will download models in the background"
Write-Host "- To view logs: docker compose logs -f"
Write-Host "- To stop services: docker compose down"
Write-Host "- To view container status: docker compose ps" 
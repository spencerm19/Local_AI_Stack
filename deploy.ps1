param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    
    [Parameter(Mandatory=$true)]
    [string]$Username,
    
    [Parameter(Mandatory=$false)]
    [string]$RemotePath = "/home/$Username",

    [Parameter(Mandatory=$false)]
    [ValidateSet('cpu', 'gpu-nvidia', 'gpu-amd')]
    [string]$Profile = 'cpu'
)

# Function to check command execution status
function Test-CommandExecution {
    param(
        [string]$Command,
        [string]$ErrorMessage
    )
    try {
        $output = Invoke-Expression $Command
        if ($LASTEXITCODE -ne 0) {
            Write-Error "$ErrorMessage. Exit code: $LASTEXITCODE"
            exit 1
        }
        return $output
    }
    catch {
        Write-Error "$ErrorMessage. Error: $_"
        exit 1
    }
}

# Check if required commands exist
$requiredCommands = @('ssh', 'scp')
foreach ($cmd in $requiredCommands) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Error "Required command '$cmd' not found. Please ensure OpenSSH is installed."
        exit 1
    }
}

# Test SSH connection
Write-Host "Testing SSH connection..."
$testSSH = "ssh -q ${Username}@${ServerIP} exit"
Test-CommandExecution -Command $testSSH -ErrorMessage "Failed to connect via SSH"

# Create project directory name
$projectDir = "Local_AI_Stack"

# Ensure the remote path exists
Write-Host "Creating remote directory..."
$sshCommand = "ssh ${Username}@${ServerIP} 'mkdir -p $RemotePath/$projectDir'"
Test-CommandExecution -Command $sshCommand -ErrorMessage "Failed to create remote directory"

# Transfer the files
Write-Host "Transferring files to server..."
$sourceDir = $PSScriptRoot  # Gets the directory where this script is located
$scpCommand = "scp -r `"$sourceDir/*`" ${Username}@${ServerIP}:${RemotePath}/$projectDir/"
Test-CommandExecution -Command $scpCommand -ErrorMessage "Failed to transfer files"

# Make the start script executable and set correct permissions
Write-Host "Setting up permissions..."
$setupCommands = @(
    "chmod +x ${RemotePath}/$projectDir/start.sh",
    "chmod 600 ${RemotePath}/$projectDir/env*"
)
foreach ($cmd in $setupCommands) {
    $sshExec = "ssh ${Username}@${ServerIP} '$cmd'"
    Test-CommandExecution -Command $sshExec -ErrorMessage "Failed to set permissions"
}

# Create .env file from template if it doesn't exist
Write-Host "Setting up environment file..."
$setupEnv = @(
    "cd ${RemotePath}/$projectDir",
    "mv 'env template' env.template 2>/dev/null || true",
    "if [ ! -f .env ]; then cp env.template .env; fi"
)
$envSetup = "ssh ${Username}@${ServerIP} '$($setupEnv -join ' && ')'"
Test-CommandExecution -Command $envSetup -ErrorMessage "Failed to setup environment file"

Write-Host "`nDeployment complete!" -ForegroundColor Green
Write-Host "`nNext steps:"
Write-Host "1. SSH into your server:" -NoNewline -ForegroundColor Yellow
Write-Host " ssh ${Username}@${ServerIP}"
Write-Host "2. Navigate to the directory:" -NoNewline -ForegroundColor Yellow
Write-Host " cd ${RemotePath}/$projectDir"
Write-Host "3. Edit the .env file:" -NoNewline -ForegroundColor Yellow
Write-Host " nano .env"
Write-Host "4. Start the services:" -NoNewline -ForegroundColor Yellow
Write-Host " sudo ./start.sh $Profile"

Write-Host "`nImportant Notes:" -ForegroundColor Cyan
Write-Host "- Make sure to update the .env file with your specific configuration"
Write-Host "- For GPU support, ensure appropriate drivers are installed on the server"
Write-Host "- The default profile is 'cpu'. Use -Profile parameter to specify 'gpu-nvidia' or 'gpu-amd'"
Write-Host "- Initial startup may take some time as Docker images are pulled and Ollama models are downloaded" 
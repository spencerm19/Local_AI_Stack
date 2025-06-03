param(
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    
    [Parameter(Mandatory=$true)]
    [string]$Username,
    
    [Parameter(Mandatory=$false)]
    [string]$RemotePath = "/home/$Username"
)

# Ensure the remote path exists
$sshCommand = "ssh ${Username}@${ServerIP} 'mkdir -p $RemotePath'"
Write-Host "Creating remote directory..."
Invoke-Expression $sshCommand

# Transfer the files
Write-Host "Transferring files to server..."
$sourceDir = $PSScriptRoot  # Gets the directory where this script is located
$scpCommand = "scp -r `"$sourceDir/*`" ${Username}@${ServerIP}:${RemotePath}/freya_ai/"
Write-Host "Executing: $scpCommand"
Invoke-Expression $scpCommand

# Make the start script executable on the remote server
Write-Host "Making start.sh executable..."
$chmodCommand = "ssh ${Username}@${ServerIP} 'chmod +x ${RemotePath}/freya_ai/start.sh'"
Invoke-Expression $chmodCommand

Write-Host "`nDeployment complete!"
Write-Host "To start the services on your server:"
Write-Host "1. SSH into your server: ssh ${Username}@${ServerIP}"
Write-Host "2. Navigate to the directory: cd ${RemotePath}/freya_ai"
Write-Host "3. Edit the .env file: nano .env"
Write-Host "4. Start the services: sudo ./start.sh [cpu|gpu-nvidia|gpu-amd]" 
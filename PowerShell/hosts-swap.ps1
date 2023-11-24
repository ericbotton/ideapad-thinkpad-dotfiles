
###
## .ps1
###
# Get the current user
$user = $env:USERNAME

# Check if the user is an administrator
if (-not ([Security.Principal.WindowsPrincipal]::GetCurrent().IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator))) {
  Write-Host "You must be an administrator to run this script."
  exit 1
}

# Get the current date and time
$current_date_time = Get-Date -Format "yyyy-MM-dd_HH:mm:ss"

# Create a backup of the hosts file
Copy-Item "$env:windir\system32\drivers\etc\hosts" "$env:windir\system32\drivers\etc\hosts.bak.$current_date_time"

# Download the new hosts file
Invoke-WebRequest -Uri https://example.com/hosts -OutFile hosts

# Replace the hosts file
Move-Item hosts "$env:windir\system32\drivers\etc\hosts"

# Restart the networking service
Restart-Service -Name "Network"

# Check if the hosts file was replaced successfully
if (Test-Path "$env:windir\system32\drivers\etc\hosts") {
  Write-Host "The hosts file was replaced successfully."
} else {
  Write-Host "Failed to replace the hosts file."
}

# download the bad ip list

#Invoke-WebRequest -Uri https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt -UseBasicParsing 2>$null | Select-String -Pattern '^[^#].*$' | Select-String -Pattern '\S[^1-2]$' -NotMatch | ForEach-Object { $_.Line.Split()[0] }

$ipsumFilename = "$env:TEMP\ipsum.txt"
Invoke-WebRequest -Uri https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt -UseBasicParsing -OutFile $ipsumFilename
$ipsumArray = $( Get-Content $ipsumFilename | Select-String -Pattern '^[^#].*$' | Select-String -Pattern '\S[^1-2]$' -NotMatch | ForEach-Object { $_.Line.Split()[0] } )

<#
Here’s what each part of the command does:

Invoke-WebRequest is the PowerShell equivalent of curl. It retrieves the contents of the specified URL.
The -UseBasicParsing parameter is used to parse the HTML content without Document Object Model (DOM) parsing.
Select-String is the PowerShell equivalent of grep. It searches for a specified pattern in a string or file.
The first Select-String command filters out lines that start with a hash symbol (#) using the pattern '^[^#].*$'.
The second Select-String command filters out lines that end with a space followed by either 1 or 2 using the pattern '\S[^1-2]$'.
Finally, ForEach-Object is used to split each line into words and select only the first word using .Line.Split()[0].
Please note that this command is not an exact equivalent of the given bash command, but it should produce similar results.
#>

foreach ( $ipAddress in $ipsumArray )
{
netsh advfirewall firewall add rule name="Block BAD IP addresses" dir=in interface=any action=block remoteip=$ipAddress
}

<# 
To block a long list of IP addresses using Windows Firewall, you can use PowerShell to create a script that contains the IP addresses you want to block and then import it into Windows Firewall. Here are the steps to do so:

Open Notepad or any other text editor.
Type the following command in the text editor: Get-Content -Path "C:\path\to\ip_list.txt" | ForEach-Object { New-NetFirewallRule -DisplayName "Block IP Address $_" -Direction Inbound -Action Block -RemoteAddress $_ }.
Replace "C:\path\to\ip_list.txt" with the path to your file containing the list of IP addresses you want to block.
Save the file with a .ps1 extension (e.g., block_ips.ps1).
Open PowerShell as an administrator.
Run the following command: Set-ExecutionPolicy RemoteSigned.
Run the following command: .\block_ips.ps1.
The script will import all of the IP addresses into Windows Firewall and create a new rule for each one.
This method is useful if you have a long list of IP addresses that you want to block, as it allows you to automate the process and avoid having to manually create a new rule for each IP address
#>
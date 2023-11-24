    # So you can now add a blocking rule to your Windows Firewall for multiple websites at once:

$SitesToBlock = "dailycaller.com","msn.com","newsmax.com"
foreach ($Site in $SitesToBlock) {
    $IPAddress = Resolve-DnsName -NoHostsFile -Name $Site | Select-Object -ExpandProperty IPAddress
    New-NetFirewallRule -DisplayName "blocksite" -Direction Outbound –LocalPort Any -Protocol Any -Action Block -RemoteAddress $IPAddress
    New-NetFirewallRule -DisplayName "blocksite" -Direction  Inbound –LocalPort Any -Protocol Any -Action Block -RemoteAddress $IPAddress
}
    # I have added the –NoHostsFile parameter to the Resolve-DnsName cmdlet in order not to use the hosts file for resolving.

<#
    # List "blocksite" rules
    Get-NetFirewallRule  | Where { $_.DisplayName -eq "blocksite" }

    # Remove "blocksite" rules
    Remove-NetFirewallRule -DisplayName "blocksite"
#>

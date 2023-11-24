<#
    You can add new lines containing website URLs to your hosts file using such a .bat file:

    @echo off
    set hostspath=%windir%\System32\drivers\etc\hosts
    echo 127.0.0.1 www.rawstory.com >> %hostspath%
    echo 127.0.0.1 rawstory.com >> %hostspath%
    exit

    Or you can use the following PowerShell functions to automatically block specific websites in your hosts file.
#>

Function BlockSiteHosts ( [Parameter(Mandatory=$true)]$Url) {
    $hosts = 'C:\Windows\System32\drivers\etc\hosts'
    $is_blocked = Get-Content -Path $hosts | Select-String -Pattern ([regex]::Escape($Url))
    If(-not $is_blocked) {
        $hoststr="127.0.0.1 ” + $Url
        Add-Content -Path $hosts -Value $hoststr
    }
}

Function UnBlockSiteHosts ( [Parameter(Mandatory=$true)]$Url) {
    $hosts = 'C:\Windows\System32\drivers\etc\hosts'
    $is_blocked = Get-Content -Path $hosts |
    Select-String -Pattern ([regex]::Escape($Url))
    If($is_blocked) {
        $newhosts = Get-Content -Path $hosts | Where-Object {
            $_ -notmatch ([regex]::Escape($Url))
        }
        Set-Content -Path $hosts -Value $newhosts
    }
}

<#
    To add a website to the list of blocked URLs, just execute the command:

    BlockSiteHosts ("huffpost.com")

    To unblock the website, run:

    UnBlockSiteHosts ("huffpost.com")

    You can also create a Firewall rule that blocks the connection to the website using PowerShell:

    New-NetFirewallRule -DisplayName "blocksite" -Direction Outbound –LocalPort Any -Protocol Any -Action Block -RemoteAddress 104.244.42.129, 104.244.42.0/24


    In order not to resolve the website names into IP addresses manually, you can use the Resolve-DnsName PowerShell cmdlet to get the website IP addresses:

    Resolve-DnsName "huffpost.com"| Select-Object -ExpandProperty IPAddress


    Thus, you can convert the name of the website into its IP addresses and add a block rule to the firewall settings:
#>

Function SetFirewallRule ( [Parameter(Mandatory=$true)]$Url) {
    $IPAddress = Resolve-DnsName $Url | Select-Object -ExpandProperty IPAddress
    New-NetFirewallRule -DisplayName "blocksite" -Direction Outbound –LocalPort Any -Protocol Any -Action Block -RemoteAddress $IPAddress
    New-NetFirewallRule -DisplayName "blocksite" -Direction  Inbound –LocalPort Any -Protocol Any -Action Block -RemoteAddress $IPAddress 
}

    # List "blocksite" rules
Function GetBlocksiteRules () {
    Get-NetFirewallRule  | Where { $_.DisplayName -eq "blocksite" }
}
    # Remove "blocksite" rules
Remove-NetFirewallRule -DisplayName "blocksite"

    # So you can now add a blocking rule to your Windows Firewall for multiple websites at once:

 Function SetFirewallRuleList ( [Parameter(Mandatory=$true)]$UrlList) {  
    $SitesToBlock = "www.dailycaller.com","www.msn.com","www.newsmax.com"
    foreach ($Site in $SitesToBlock) {
        $IPAddress = Resolve-DnsName -NoHostsFile -Name $Site | Select-Object -ExpandProperty IPAddress
        New-NetFirewallRule -DisplayName "blocksite" -Direction Outbound –LocalPort Any -Protocol Any -Action Block -RemoteAddress $IPAddress
        New-NetFirewallRule -DisplayName "blocksite" -Direction  Inbound –LocalPort Any -Protocol Any -Action Block -RemoteAddress $IPAddress
    }
    # I have added the –NoHostsFile parameter to the Resolve-DnsName cmdlet in order not to use the hosts file for resolving.
}


$user = Read-Host -Prompt "Username: "
$password = Read-Host -Prompt "Password: "

$computer1 = "Print Server1"
$computer2 = "testPrinterv1"

if (Connect-VIServer 10.156.4.65 -User $user -Password $password) 
{
    Write-Host "Connected succesfully!"
    Start-Sleep -Seconds 2
}
else
    {break}


while($true)
{
    $VM1 = Get-VM -Name $computer1
    $VM2 = Get-VM -Name $computer2
    $status1 = $VM1.PowerState
    $status2 = $VM2.PowerState


    if ($status1 -eq "PoweredOn")
        {Write-Host "Virtual Machine: $computer1 is Online"}
    else
        {Write-Host "Virtual Machine: $computer1 is Offline"}
    if ($status2 -eq "PoweredOn")
        {Write-Host "Virtual Machine: $computer2 is Online"}
    else
        {Write-Host "Virtual Machine: $computer2 is Offline"}


    if ($status1 -eq "PoweredOn")
    {
        Start-Sleep -Seconds 2
        Write-Host "Pinging $computer1 'hidden' IP Address..."
        if (!(Test-Connection -Cn 10.156.4.98 -BufferSize 16 -Count 3 -ea 0 -Quiet))
        {
            Write-Host "$computer1 returned no response";
            if ($status2 -eq "PoweredOn")
                {Write-Host "Keeping $computer2 alive"}
            else{
                Write-Host "Powering On $computer2";
                Start-VM -VM $computer2}
        }
        else 
        {
            Write-Host "Ping successful";
            if ($status2 -eq "PoweredOn")
            {
                Write-Host "$computer2 is Online. Powering it off."
                Shutdown-VMGuest -VM $computer2 -Confirm:$false -EV Err -EA SilentlyContinue
            }
            Start-Sleep -Seconds 1
            Write-Host "Pinging $computer1 primary IP Address..."
            if (!(Test-Connection -Cn 10.156.4.97 -BufferSize 16 -Count 3 -ea 0 -Quiet))
            {
                Write-Host "$computer1 returned no response"
                Start-Sleep -Seconds 1
            }
            else
                {Write-Host "Ping successful"}
            }
    }
    else 
    {
        if ($status2 -eq "PoweredOff")
        {
            Write-Host "Both VMs seems to be offline."
            Write-Host "Powering On $computer2"
            Start-VM -VM $computer2
        }
        Write-Host "Pinging $computer2..."
        if (!(Test-Connection -Cn 10.156.4.97 -BufferSize 16 -Count 3 -ea 0 -Quiet))
        {
            Write-Host "Could not ping $computer2"
            Start-Sleep -Seconds 2
            Write-Host "This could mean it is still booting up, or that NIC needs to be restarted."
            Start-Sleep -Seconds 2
            Write-Host "Will attempt to ping again in 10 seconds."
            Start-Sleep -Seconds 2
            Write-Host "If this ping is not successful soon, you have to look into it!"
        }
        else
            {Write-Host "Ping successful"}
    }
    Start-Sleep -Seconds 1
    Write-Host "Waiting 10 seconds"
    Start-Sleep -Seconds 10
    cls
    }
### Required dependency ###
# robotframework-sshlibrary

from SSHLibrary import SSHLibrary
import time
ssh = SSHLibrary()
ssh.open_connection("10.156.4.65")
username = input("Username: ")
password = input("Password: ")
print("\033c")
ssh.login(username, password)

#The loop
while True:
    PSRV1 = ssh.execute_command("vim-cmd vmsvc/power.getstate 20", return_stdout=True)
    PSRV2 = ssh.execute_command("vim-cmd vmsvc/power.getstate 24", return_stdout=True)
    time.sleep(2)
    print("\033c")
    if "Powered on" in PSRV1:
        print("Virtual Machine: PSRV1 is Online")
    else:
        print("Virtual Machine: PSRV1 is Offline")
    if "Powered on" in PSRV2:
        print("Virtual Machine: PSRV2 is Online")
    else:
        print("Virtual Machine: PSRV2 is Offline")
    print(" ")
    # If PSRV1 is ON:
    if "Powered on" in PSRV1:
        # Ping PSRV1 to see if its actually ready. If no packets received = Power on PSRV2.
        # This could be relevant if PSRV1 is updating etc. VM will still be online, but it won't be able to handle printing in its state.
        print("Pinging PSRV1...")
        pingResponse = ssh.execute_command("ping 10.156.4.98", return_stdout=True)
        if "100% packet loss" in pingResponse:
            if "Powered on" in PSRV2:
                print("Virtual Machine: PSRV1 returned no response. Keeping Virtual Machine: PSRV2 alive")
            else:
                print("Virtual Machine: PSRV1 returned no response\nPowering On Virtual Machine: PSRV2\n")
                ssh.start_command("vim-cmd vmsvc/power.on 24")
        else:
            print("Ping successful")
            if "Powered on" in PSRV2:
                print("Virtual Machine: PSRV2 is Online")
                ssh.start_command("vim-cmd vmsvc/power.off 24")
                print("Powering Off Virtual Machine: PRSV2")
    # If PSRV1 is OFF:
    else:
        # If PSRV2 is ON:
        if "Powered on" in PSRV2:
            pass
        else:
        # If PSRV2" is OFF:
            print("PSRV1 appears to be offline.\nPowering Up Virtual Machine: PSRV2")
            ssh.start_command("vim-cmd vmsvc/power.on 24")
    time.sleep(2)
    print("Waiting 10 seconds")
    time.sleep(10)
ssh.close_connection()

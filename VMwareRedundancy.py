### Required dependency ###
# 

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
    PSRV2 = ssh.execute_command("vim-cmd vmsvc/power.getstate 19", return_stdout=True)
    if "Powered on" in PSRV1:
        print("Virtual Machine: PSRV1 is Online")
        if "Powered on" in PSRV2:
            print("Virtual Machine: PSRV2 is Online")
            ssh.start_command("vim-cmd vmsvc/power.off 19")
            print("Powering Off Virtual Machine: PRSV2")
        else:
            print("Virtual Machine: PSRV2 is Offline")
    else:
        print("Virtual Machine: PSRV1 is Offline")
        if "Powered on" in PSRV2:
            print("Virtual Machine: PSRV2 is Online")
        else:
            print("Virtual Machine: PSRV2 is Offline")
            print("Pinging PSRV1...")
            pingResponse = ssh.execute_command("ping 10.156.4.97", return_stdout=True)
            if "100% packet loss" in pingResponse:
                print("Virtual Machine: PSRV1 is returned no response\nPowering On Virtual Machine: PSRV2\n")
                ssh.start_command("vim-cmd vmsvc/power.on 19")
    
    time.sleep(10)
    print(" \n")
    print(" \n")
ssh.close_connection()

### Required dependency ###
# 

from SSHLibrary import SSHLibrary
import time
ssh = SSHLibrary()
ssh.open_connection("10.156.4.79")
ssh.login("root", "Qwerty12345!")

#The loop
while True:
    PSRV1 = ssh.execute_command("vim-cmd vmsvc/power.getstate 7", return_stdout=True)
    PSRV2 = ssh.execute_command("vim-cmd vmsvc/power.getstate 6", return_stdout=True)
    if "Powered on" in PSRV1:
        print("Virtual Machine: PSRV1 is Online\nVirtual Machine: PSRV2 is Offline\n")
        if "Powered on" in PSRV2:
            ssh.start_command("vim-cmd vmsvc/power.off 6")
            print("Powering Off Virtual Machine: PRSV2\n")
    else:
        if "Powered on" in PSRV2:
            print("Virtual Machine: PSRV1 is Offline\nVirtual Machine: PSRV2 is Online\n")
        else:
            print("Virtual Machine: PSRV1 is Offline\nVirtual Machine: PSRV2 is Offline\nPowering On Virtual Machine: PSRV2\n")
            ssh.start_command("vim-cmd vmsvc/power.on 6")
    time.sleep(10)
ssh.close_connection()
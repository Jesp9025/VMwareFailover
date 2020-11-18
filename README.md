# *This is part of a school project!*

# VMware Redundancy

Python version and powershell version of print server failover.

v2 (only PowerShell):Removed the restart of network adapter.
IP duplicate has been fixed in Windows Registry on print servers with ArpRetryCount 0 and IPAutoconfigurationEnabled 0.

(It now allows the 2 servers to be running at the same time with the same IP address)

# What is this

These scripts will automate a failover for 2 identical servers (Cloned VM on ESXI).
In our case it is for 2 print servers that needs to have high uptime and redundancy.

Server1 is setup with 2 addresses (10.156.4.97, 10.156.4.98), Server2 is setup with 1 address (10.156.4.97).

# Why the second IP address on Server1

The second address on server1 is needed to ping the server, since server2 also has the same primary IP address as server1 (10.156.4.97),
and pinging .97 while secondary VM is up and running, will give a false positive of the primary VM's state.

# How does it work

Script checks if primary VM is on, and if not, power up secondary VM.

If primary VM is on, it will ping its second IP address to see if it is actually running normally.
A case of ping failing could mean the OS is updating, rebooting or in fail mode.

if ping succeeds, all is good and nothing else happens.

v1 only: If .98 is pingable, but .97 is not, if will attempt to restart the network adapter on server1 (duplicate IP error).

v2: Has been fixed as described earlier.

If ping fails, it will check if secondary VM is powered up, and if not, will power it up.

It will then continue in a loop and attempt to see if primary VM is on and pingable, and shutdown secondary VM if it is indeed pingable.

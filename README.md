# IPAUTH-API

IPAUTH-API is a tool to help in the SSH access control. Add the current requested IP in a 'whitelist' for access SSH port.

How it works:

  - Creates a sqlite data base with user details (username, key, skey, old IP and current IP)
  - Users must be in the local system
  - Uses iptables to control the firewall access for the SSH port
  - The owner running the ipauth_api.py must have access to iptables via sudo

Installation:

Create IPtables chain IPAUTH-API and redirect the SSH port to IPAUTH-API chain
```sh
# iptables -A IPAUTH-API -j reject
# iptables -A INPUT -p tcp -m tcp --dport SSH_PORT -j IPAUTH-API
```

Add owner file to sudo:
```sh
# visudo
// Add the following entry to your sudo file
username ALL= NOPASSWD: /sbin/iptables
```

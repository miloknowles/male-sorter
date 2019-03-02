# Male Sorter

Sort your males into bins.

## Troubleshooting
```bash

# Put this in /etc/network/interfaces
# interfaces(5) file used by ifup(8) and ifdown(8)
auto lo
#iface lo inet loopback
#iface eth0 inet static
#   address 192.168.2.1
#   netmask 255.255.255.0
iface lo inet loopback
iface enx0014d1dad9a2 inet static
    address 192.168.2.1
    netmask 255.255.255.0

sudo ifdown enx0014d1dad9a2
sudo ifup enx0014d1dad9a2
```

## Networking
User: xilinx
Password: xilinx
Hostname: pynq

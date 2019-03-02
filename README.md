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

### Networking
User: xilinx
Password: xilinx
Hostname: pynq

### Connecting to WIFI
sudo ifconfig wlan0
sudo ifdown wlan0 # Turn of wlan0
iwconfig wlan0 essid MIT # This is the only network I could get to work
dhclient wlan0 # Didn't get any output
ip addr

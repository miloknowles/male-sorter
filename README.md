# Male Sorter

Sort your males into bins.

## Troubleshooting
```bash

# Put this in /etc/network/interfaces
# interfaces(5) file used by ifup(8) and ifdown(8)
auto lo
iface lo inet loopback
iface enx0014d1dad9a2 inet static
    address 192.168.2.1
    netmask 255.255.255.0

sudo ifdown enx0014d1dad9a2
sudo ifup enx0014d1dad9a2
```

### Install packages with Pip
```bash
# Must use the same Python that Jupyter is running!
# This was the only way I could get Jupyter to import properly...
sudo pip3  install pytesseract
```

### Networking
```
User: xilinx
Password: xilinx
Hostname: pynq_milo
```

### Connecting to WIFI
```bash
# sudo ifconfig wlan0
sudo ifdown wlan0 # Turn of wlan0
sudo iwconfig wlan0 essid MIT # This is the only network I could get to work
sudo dhclient wlan0 # Didn't get any output
# ip addr
```

Link: https://linoxide.com/linux-how-to/connect-wifi-terminal-ubuntu-16-04/

### Installing Tesseract
- Install C++ library here: https://github.com/tesseract-ocr/tesseract/wiki
- Had to ```sudo apt update``` after adding to apt sources
- Then ```sudo pip3  install pytesseract```
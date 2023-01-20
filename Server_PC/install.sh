#!/bin/bash


D=`dirname "${BASH_SOURCE[0]}"`


#https://derushadigital.com/other%20projects/2019/02/19/RPi-USBIP-ZWave.html

sudo apt -y install usbip python3-pyudev
#sudo modprobe usbip_host
#echo 'usbip_host' | sudo tee -a /etc/modules >> /dev/null

sudo apt -y install linux-tools-`uname -r`

sudo modprobe usbip_host	###
sudo modprobe vhci-hcd
echo 'usbip_host' | sudo tee -a /etc/modules >> /dev/null	###
echo 'vhci-hcd' | sudo tee -a /etc/modules >> /dev/null

sudo mkdir -p /usr/local/sbin/
sudo cp $D/usbipd_service.py /usr/local/sbin/
sudo mkdir -p /usr/local/share/usbip_services
sudo cp $D/../common/settings.csv /usr/local/share/usbip_services
sudo cp $D/usbipd.service /lib/systemd/system/

# reload systemd, enable, then start the service
sudo systemctl --system daemon-reload
sudo systemctl enable usbipd.service
sudo systemctl start usbipd.service

# For debug:
#/usr/sbin/usbip list -p -l
#systemctl status usbipd.service | less

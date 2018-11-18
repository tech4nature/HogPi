#!/bin/bash

function InstallI2S {

sudo echo "dtparam=i2s=on" >> /boot/config.txt
sudo echo "snd-bcm2835" >> /etc/modules

sudo echo "sudo apt-get update" >> /etc/rc.local
sudo echo "sudo apt-get install rpi-update -y" >> /etc/rc.local
sudo echo "sudo rpi-update" >> /etc/rc.local
sudo echo "sudo bash /usr/bin/i2s_2.sh" >> /etc/rc.local

sudo reboot

}

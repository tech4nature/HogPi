#!/bin/bash

function InstallI2S {

sudo echo "dtparam=i2s=on" >> /boot/config.txt
sudo echo "snd-bcm2835" >> /etc/modules

sudo apt-get update
sudo apt-get install rpi-update -y
sudo rpi-update

sudo reboot

}

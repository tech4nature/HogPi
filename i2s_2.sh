#!/bin/bash

sudo echo "sudo apt-get install git bc libncurses5-dev -y" >> /etc/rc.local
sudo echo "sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source" >> /etc/rc.local
sudo echo "sudo chmod +x /usr/bin/rpi-source" >> /etc/rc.local
sudo echo "/usr/bin/rpi-source -q --tag-update" >> /etc/rc.local
sudo echo "rpi-source --skip-gcc" >> /etc/rc.local
sudo echo "sudo mount -t debugfs debugs /sys/kernel/debug" >> /etc/rc.local
sudo echo "git clone https://github.com/PaulCreaser/rpi-i2s-audio /home/pi/rpi-i2s-audio" >> /etc/rc.local
sudo echo "cd /home/pi/rpi-i2s-audio" >> /etc/rc.local
sudo echo "make -C /lib/modules/$(uname -r )/build M=$(pwd) modules" >> /etc/rc.local
sudo echo "sudo insmod my_loader.ko" >> /etc/rc.local
sudo echo "sudo cp my_loader.ko /lib/modules/$(uname -r)" >> /etc/rc.local
sudo echo "echo 'my_loader' | sudo tee --append /etc/modules > /dev/null" >> /etc/rc.local
sudo echo "sudo depmod -a" >> /etc/rc.local
sudo echo "sudo modprobe my_loader" >> /etc/rc.local

sudo reboot

#!/bin/bash

function InstallI2S_Part2 {

sudo apt-get install git bc libncurses5-dev -y
sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source
sudo chmod +x /usr/bin/rpi-source
/usr/bin/rpi-source -q --tag-update
rpi-source --skip-gcc
sudo mount -t debugfs debugs /sys/kernel/debug
git clone https://github.com/PaulCreaser/rpi-i2s-audio /home/pi/rpi-i2s-audio
cd /home/pi/rpi-i2s-audio
make -C /lib/modules/$(uname -r )/build M=$(pwd) modules
sudo insmod my_loader.ko
sudo cp my_loader.ko /lib/modules/$(uname -r)
echo 'my_loader' | sudo tee --append /etc/modules > /dev/null
sudo depmod -a
sudo modprobe my_loader

sudo reboot

}

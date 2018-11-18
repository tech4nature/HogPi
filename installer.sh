#!/bin/bash

. whiptail.sh

echo "Installing prerequisites..."
sudo apt update
sudo apt install whiptail git mercurial wget -y
cp *.sh /usr/bin/

WelcomeScreen
MainMenu



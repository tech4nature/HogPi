#!/bin/bash

. FFMpeg.sh
. i2s.sh

function WelcomeScreen() {

	whiptail --title "Welcome to HogPi" --fb --msgbox "This is the installer for HogPi" $(stty size)
}

function MainMenu() {

Menu1=$(whiptail --title "HogPi Installer" --fb --menu "Choose an option" $(stty size) $(( $(tput lines) - 8)) \
        "Install" "Install a Package" \
        "Update" "Update your system" \
        "Exit" "Exit the installer" 3>&1 1>&2 2>&3)
case $Menu1 in
        Install)
            InstallMenu1=$(whiptail --title "HogPi Installer" --fb --menu "Choose a program you would like to install." $(stty size) $(( $(tput lines) - 8))  \
		   "FFmpeg" "A multimedia library" \
		   "I2S" "Library for mic" \
		   "Fritzing" "A tools for drwaing circuits" \
		   "Code::Blocks" "A C/C++/Fortan IDE for Raspberry Pi" 3>&1 1>&2 2>&3)
			
		case $InstallMenu1 in
			FFmpeg)
				InstallFFmpeg
				MainMenu
			;;
			I2S)
				InstallI2S
			;;
			Fritzing)
				sudo apt install fritzing fritzing-data fritzing-parts -y
				MainMenu
			;;
			Code::Blocks)
				sudo apt install codeblocks -y
				MainMenu
			;;
		esac
        ;;
        Update)
            sudo apt update
			sudo apt upgrade -y
			sudo apt clean -y
			sudo apt autoremove -y
            whiptail --title "HogPi Installer" --fb --msgbox "Your machine has been updated to the latest version" $(stty size)
			MainMenu
        ;;
        Exit)
            whiptail --title "HogPi Installer" --fb --msgbox "Goodbye. Thank you for using HogPi" $(stty size)
        ;;
esac

}

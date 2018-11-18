#!/bin/bash

. FFMpeg.sh
. i2s.sh

eval `resize`
function WelcomeScreen() {

	whiptail --title "Welcome to HogPi" --fb --msgbox "This is the installer for HogPi" $LINES $COLUMNS

}

function MainMenu() {

Menu1=$(whiptail --title "HogPi Installer" --fb --menu "Choose an option" $LINES $COLUMNS $(( $LINES - 8 )) \
        "Install" "Install a Package" \
        "Update" "Update your system" \
        "Exit" "Exit the installer" 3>&1 1>&2 2>&3)
case $Menu1 in
        Install)
            InstallMenu1=$(whiptail --title "HogPi Installer" --fb --menu "Choose a program you would like to install." $LINES $COLUMNS $(( $LINES - 8 )) \
		   "FFmpeg" "A multimedia library" \
		   "I2S" "Library for mic" \
		   "Code::Blocks" "A C/C++/Fortan IDE for Raspberry Pi" 3>&1 1>&2 2>&3)
			
		case $InstallMenu1 in
			FFmpeg)
				InstallFFmpeg
				MainMenu
			;;
			I2S)
				InstallI2S
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
            whiptail --title "HogPi Installer" --msgbox "Your machine has been updated to the latest version" 8 45
			MainMenu
        ;;
        Exit)
            whiptail --title "HogPi Installer" --msgbox "Goodbye. Thank you for using HogPi" 8 45
        ;;
esac

}



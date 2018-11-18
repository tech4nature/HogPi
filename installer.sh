#!/bin/bash

function InstallFFmpeg(){
	echo "Install Dependencies"
	
	sudo apt-get update
	sudo apt-get upgrade -y
	sudo apt-get install autoconf automake build-essential libass-dev libfreetype6-dev libmp3lame-dev libomxil-bellagio-dev libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev -y
	
	echo "Clone git repo"
	
	git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
	cd ffmpeg
	mkdir dependencies
	cd dependencies
	mkdir output
	
	echo "Compile libx264"
	
	git clone http://git.videolan.org/git/x264.git
	cd x264/
	./configure --enable-static --prefix=/home/pi/ffmpeg/dependencies/output/
	make -j4
	make install
	cd ..
	
	echo "Compile ALSA"
	
	wget ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.1.1.tar.bz2
	tar xjf alsa-lib-1.1.1.tar.bz2
	cd alsa-lib-1.1.1/
	./configure --prefix=/home/pi/ffmpeg/dependencies/output
	make -j4
	make install
	cd ..
	
	echo "Compile FDK-AAC"
	
	sudo apt-get install pkg-config autoconf automake libtool -y
	git clone https://github.com/mstorsjo/fdk-aac.git
	cd fdk-aac
	./autogen.sh
	./configure --enable-shared --enable-static
	make -j4
	sudo make install
	sudo ldconfig
	cd ..
	
	echo "Compile FFMPEG"
	
	cd ..
	./configure --prefix=/home/pi/ffmpeg/dependencies/output --enable-gpl --enable-libx264 --enable-nonfree --enable-mmal --enable-libfdk_aac --enable-omx --enable-omx-rpi --enable-libmp3lame --extra-cflags="-I/home/pi/ffmpeg/dependencies/output/include" --extra-ldflags="-L/home/pi/ffmpeg/dependencies/output/lib" --extra-libs="-lx264 -lpthread -lm -ldl"
	make -j4
	make install
	
}

echo "Installing prerequisites..."
sudo apt install whiptail git mercurial -y

eval `resize`
whiptail --title "Welcome to HogPi" --fb --msgbox "This is the installer for HogPi" $LINES $COLUMNS
Menu1=$(whiptail --title "HogPi Installer" --fb --menu "Choose an option" $LINES $COLUMNS $(( $LINES - 8 )) \
        "Install" "Install a Package" \
        "Update" "Update your system" \
        "Exit" "Exit the installer" 3>&1 1>&2 2>&3)
case $Menu1 in
        Install)
            echo "Option 1"
            InstallMenu1=$(whiptail --title "HogPi Installer" --fb --menu "Choose an option" $LINES $COLUMNS $(( $LINES - 8 )) \
		   "FFmpeg" "A multimedia library" \
		   "Code::Blocks" "A C/C++/Fortan IDE for Raspberry Pi" 3>&1 1>&2 2>&3)
			
		case $InstallMenu1 in
			FFmpeg)
				InstallFFmpeg
			;;
			Code::Blocks)
				sudo apt install codeblocks -y
			;;
		esac
        ;;
        Update)
            sudo apt update
			sudo apt upgrade -y
			sudo apt clean -y
			sudo apt autoremove -y
            whiptail --title "HogPi Installer" --msgbox "Your machine has been updated to the latest version" 8 45
        ;;
        Exit)
            whiptail --title "HogPi Installer" --msgbox "Goodbye. Thank you for using HogPi" 8 45
        ;;
esac


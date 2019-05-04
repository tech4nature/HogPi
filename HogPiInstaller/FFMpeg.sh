#!/bin/bash

tar=/bin/tar
wget=/usr/bin/wget

function InstallFFmpeg {
	echo "Install Dependencies"

	sudo apt-get update
	sudo apt-get upgrade -y
	sudo apt-get install autoconf automake build-essential libass-dev libfreetype6-dev libmp3lame-dev libomxil-bellagio-dev libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev -y

	echo "Clone git repo"
	cd ~

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

	wget ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.1.7.tar.bz2
	tar xjf alsa-lib-1.1.7.tar.bz2
	cd alsa-lib-1.1.7/
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
	./configure --prefix=/home/pi/ffmpeg/dependencies/output --enable-gpl --enable-libmp3lame --enable-libx264 --enable-nonfree --enable-mmal --enable-libfdk_aac --enable-libfreetype --enable-omx --enable-omx-rpi --extra-cflags="-I/home/pi/ffmpeg/dependencies/output/include" --extra-ldflags="-L/home/pi/ffmpeg/dependencies/output/lib" --extra-libs="-lx264 -lpthread -lm -ldl"
	make -j4
	make install
	sudo cp ./ffmpeg ./ffprobe /usr/bin/
	sudo rm -rf ~/ffmpegu

}

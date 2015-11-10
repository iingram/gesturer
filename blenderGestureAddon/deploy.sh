#!/bin/bash

echo -n "Do you want to use a fresh install of Blender in this directory?[y/n]: "
read freshInstall

if [ "$freshInstall" == "y" ]; then 
	installPyserial="y"
	installPyYAML="y"

	echo -n "Does the zip exist in the current directory?[y/n]:"
	read zipExists


	echo -n "What is your operating system?[MacOS/Linux32/Linux64]: "
	read osType

	if [ "$osType" == "MacOS" ]; then
		echo "Downloading Blender..."
		if [ "$zipExists" == "n" ]; then
			curl -O http://ftp.halifax.rwth-aachen.de/blender/release/Blender2.76/blender-2.76b-OSX_10.6-x86_64.zip
		fi
		echo "Extracting Blender..."
		zip -d blender-2.76b-OSX_10.6-x86_64.zip "__MACOSX*"
		tar -xzf blender-2.76b-OSX_10.6-x86_64.zip
		# echo "Removing Blender download..."
		# rm blender-2.76b-OSX_10.6-x86_64.zip
		rm -rf __MACOSX/
		PYTHONPATH="blender-2.76b-OSX_10.6-x86_64/blender.app/Contents/Resources/2.76/python/lib/python3.4/"
		ADDONPATH="blender-2.76b-OSX_10.6-x86_64/blender.app/Contents/Resources/2.76/scripts/addons/"
	elif [ "$osType" == "Linux32" ]; then
		echo "Downloading Blender..."
		if [ "$zipExists" == "n" ]; then
			curl -O http://ftp.halifax.rwth-aachen.de/blender/release/Blender2.76/blender-2.76b-linux-glibc211-i686.tar.bz2
		fi
		echo "Extracting Blender..."
		tar -xzf blender-2.76b-linux-glibc211-i686.tar.bz2
		# echo "Removing Blender download..."
		# rm blender-2.76b-linux-glibc211-i686.tar.bz2
		rm -rf __MACOSX/
		PYTHONPATH="blender-2.76b-linux-glibc211-i686/2.76/python/lib/python3.4/"
		ADDONPATH="blender-2.76b-linux-glibc211-i686/2.76/scripts/addons/"
	elif [ "$osType" == "Linux64" ]; then
		echo "Downloading Blender..."
		if [ "$zipExists" == "n" ]; then
			curl -O http://ftp.halifax.rwth-aachen.de/blender/release/Blender2.76/blender-2.76b-linux-glibc211-x86_64.tar.bz2
		fi
		echo "Extracting Blender..."
		# tar -xzf blender-2.76b-linux-glibc211-x86_64.tar.bz2
		# echo "Removing Blender download..."
		rm blender-2.76b-linux-glibc211-x86_64.tar.bz2
		rm -rf __MACOSX/
		PYTHONPATH="blender-2.76b-linux-glibc211-x86_64/2.76/python/lib/python3.4/"
		ADDONPATH="blender-2.76b-linux-glibc211-x86_64/2.76/scripts/addons/"
	fi

else
	echo -n "Please enter the path to your Blender Python library: "
	read PYTHONPATH
	echo -n "Please enter the path to your Blender Addons directory: "
	read ADDONPATH
	echo -n "Do you need to install pySerial for Blender?[y/n]: "
	read installPyserial
	echo -n "Do you need to install PyYAML for Blender?[y/n]: "
	read installPyYAML
fi

if [ "$installPyserial" == "y" ]; then 
	echo "Downloading PySerial..."
	git clone "https://github.com/pyserial/pyserial.git"
	echo "Copying PySerial to the Blender Python library..."
	cp -rf pyserial/serial "$PYTHONPATH"
	echo "Removing PySerial download..."
	rm -rf pyserial
fi

if [ "$installPyYAML" == "y" ]; then 
	echo "Downloading PyYAML..."
	git clone "https://github.com/yaml/pyyaml.git"
	echo "Coying PyYAML to the Blender Python library..."
	cp -rf pyyaml/lib3/yaml "$PYTHONPATH"
	echo "Removing PyYAML download..."
	rm -rf pyyaml
fi

echo "Copying the gestureDeveloper addon to the Blender Addons directory..."
cp gestureDeveloper.py "$ADDONPATH"

echo "Finished with Blender Gesture Developer Addon deployment!"

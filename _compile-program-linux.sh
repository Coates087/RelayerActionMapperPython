# Requires at least python 3.12.4
# Only run this script if PyInstaller is installed (https://pyinstaller.org/en/stable/)
# Note: type in "bash ./_compile-program-linux.sh" in the cmd terminal. 
# ...Make sure to whiteList this directory with your anti-virus software
# Try this guide for installing the latest Python: https://tecadmin.net/how-to-install-python-3-12-on-ubuntu-debian-linuxmint/
#
mkdir -p "build"
cp "./resource_objects/RelayerIcon.ico" "./build/RelayerIcon.ico"
#
python3.12 -m PyInstaller --onefile --noconsole --icon "RelayerIcon.ico" --specpath "./build/" --distpath  "./build/dist/" main.py --name "Relayer Action Mapper PE"
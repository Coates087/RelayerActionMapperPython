@REM Requires at least Python 3.12.3 installed
@REM Only run this script if PyInstaller is installed (https://pyinstaller.org/en/stable/)
@REM Note: type in "start _compile-program-win.bat" without quotes or type "_compile-program-win.bat" in the cmd terminal. 
@REM ...Make sure to whiteList this directory with your anti-virus software

xcopy /S /Q /Y /F "./resource_objects/RelayerIcon.ico" "./build/RelayerIcon.ico"*

python -m PyInstaller --onefile --noconsole --icon "RelayerIcon.ico" --specpath "./build/" --distpath  "./build/dist/" main.py --name "Relayer Action Mapper PE"
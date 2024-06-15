@REM only run this script if PythonInstaller is installed (https://www.python.org/downloads/)
@REM Note: type in "start _compile-program-win.bat" without quotes or type "_compile-program-win.bat" in the cmd terminal. 
@REM ...Make sure to whitelist this directory with your anti-virus software

xcopy /S /Q /Y /F "./resource_objects/RelayerIcon.ico" "./build/RelayerIcon.ico"*

python -m PyInstaller --onefile --noconsole --icon "RelayerIcon.ico" --specpath "./build/" --distpath  "./build/dist/" main.py --name "Relayer Action Mapper PE"
@REM only run this script if PythonInstaller is installed
xcopy /S /Q /Y /F "./resource_objects/RelayerIcon.ico" "./build/RelayerIcon.ico"*

python -m PyInstaller --onefile --noconsole --icon "RelayerIcon.ico" --specpath "./build/" --distpath  "./build/dist/" main.py --name "Relayer Action Mapper Python"
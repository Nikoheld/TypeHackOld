@echo off
echo Installing Python...
start /wait https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
echo Python installed successfully!

echo Installing required Python packages...
pip install selenium 
pip install pynput 
pip install Controller 
pip install colorama 
pip install PyGetWindow
echo Required packages installed successfully!

echo All installations completed.
pause
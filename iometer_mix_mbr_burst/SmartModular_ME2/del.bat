REM Use at your own risk, it does a mass DELETE of everything!

SET ExcludeFiles=(icf bat)     
SET MapDrive=%cd:~0,1%
SET Directory="C:\Jenkins\IOMeter\iometer_mix_mbr-dean3dtlc\SmartModular ME2"

%MapDrive%:
cd %Directory%

attrib +a *.* /s
echo %date%
for %%i in %ExcludeFiles% do attrib -a *.%%i /s
echo %date%
del %Directory%\*.* /s /a:a /q

echo %date%
attrib +a %Directory%\*.* /s
echo %date%

for /f "usebackq" %%d in (`"dir /ad/b/s | sort /R"`) do rd "%%d"
pause
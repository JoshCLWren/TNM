@echo off
cd tnm7se\tnm7se
echo x>tnm.pid
if exist tnmgs.no goto onward
if exist tnmgs.* del tnmgs.*
if exist program\tnmgs.exe start program\tnmgs.exe

:onward
cd ..\..
start /min tnm7se\tnm7se\program\tnmdbwrp .\tnm7se\tnm7se
if not exist c:\tnm_xchg mkdir c:\tnm_xchg
goto here
:there
del tnm7se\tnm7se\dosbox.rst
:here
dosbox -exit -conf .\dosbox-0.74.conf.txt -noconsole
if exist tnm7se\tnm7se\dosbox.rst goto there
del tnm7se\tnm7se\tnmdbwrp.pid
PING localhost -n 3 >NUL

cd tnm7se\tnm7se\temp
for %%i in (*.exe) do del ..\program\%%i
for %%i in (*.exe) do move %%i ..\program
cd ..\..\..
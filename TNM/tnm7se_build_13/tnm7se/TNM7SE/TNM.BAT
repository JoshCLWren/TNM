@echo off
echo x>tnm.pid
if exist tnmgs.no goto onward
if exist tnmgs.* del tnmgs.*
if exist program\tnmgs.exe start program\tnmgs.exe
:onward
program\card
rem program\cwc
if exist tnm.pid del tnm.pid
exit

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

cd tnm7se\tnm7se
echo x>tnm.pid
subst t: c:\tnm_xchg
program\card
subst t: /d
if exist tnm.pid del tnm.pid
cd ..\..
if exist tnm.pid del tnm.pid
if exist tnm7se\tnm7se\tnmdbwrp.pid del tnm7se\tnm7se\tnmdbwrp.pid
@echo off
copy ..\..\descript\tnmmatch.inf .
copy /y c:\battools\tnmmatch.exe .
7z a tnmmatch%1.zip *.exe *.inf *.mmf
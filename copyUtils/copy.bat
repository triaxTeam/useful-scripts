@echo off
 
set "file=C:\projects\simens_test\1.BIN"
set "number=30"
 
call:# "%file%" %number%
 
exit/b
 
 
:#
 pushd "%~dp1"
 2>nul md "Copies"
 for /l %%i in (1 1 %~2) do copy/y "%~nx1" "Copies\%%i%~x1"
 popd
 goto:eof
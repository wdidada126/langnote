chcp 65001
@echo off
set arg=
set handleFile=0
:loop
if %1a==a goto :end
set x=%1
set x=%x:\=/%

echo %x%| findstr "fileList.txt" >nul && (
        set handleFile=fileList.txt
        rem arg contains
        rem set x=%x:fileList.txt=fileList.txt.new%
) || (
        rem arg not contains
)

set arg=%arg% %x%

shift
goto :loop


:end
if not "%handleFile%"=="fileList.txt" goto end2
echo handleFile %handleFile%
if exist %handleFile%.new del %handleFile%.new
@echo off&setlocal EnableDelayedExpansion
for /f "delims=" %%b in ('type %handleFile%') do (
set "str=%%b"&set "str=!str:\=/!"
echo !str!>>%handleFile%.new
)
if exist %handleFile%.new move %handleFile%.new %handleFile%
goto end3

:end2
echo handleFile0 %handleFile%

:end3
@echo on
C:\ProgramData\chocolatey\lib\rsync\tools\cwrsync_6.2.5_x64_free\bin\rsync.exe %arg%
exit 0
@echo off
setlocal
set "file_path=.\settings\username.txt"
set /p user1=<%file_path%
echo Starting Game...
echo.
for /f "delims=" %%a in ('powershell -Command "(Invoke-WebRequest 'https://raw.githubusercontent.com/kappucin/MoonMCExec/master/version.txt').Content"') do set "content=%%a"
for /f "usebackq delims=" %%A in (".\game\version.txt") do set "version=%%A"

if "%version%" equ "%content%" (
    echo  No updates, modpack version: %version% & goto success
) else (
    goto update
)

exit

:success
echo  Nickname: %user1%
.\bin\core.exe --main-dir "game" start forge:1.20.1 -u %user1% "--jvm-args=-Xmx6000M -Xms2048M" --server f1.aurorix.net --server-port 44354
echo  Game Closed! Error level: %ERRORLEVEL% Nickname: %user1%
exit

:update
echo Update availible!
echo Cloning git repo with update...
.\bin\mingit\cmd\git.exe clone https://github.com/kappucin/MoonMCExec.git
rmdir /s /q .\MoonMCExec\.git
echo Downloaded update...
echo Cleaning old version...
rem Mods
del /f /s /q .\game\mods\*.jar
rem Config
del /f /s /q .\game\config\*.toml
del /f /s /q .\game\config\*.json
rmdir /s /q .\game\config\*
rem Shaderpacks
del /f /s /q .\game\shaderpacks\*.zip
del /f /s /q .\game\shaderpacks\*.txt
rmdir /s /q .\game\shaderpacks\*
echo Updating...
rem Mods
copy /Y .\MoonMCExec\mods\*.jar .\game\mods\
rem Configs
copy /Y .\MoonMCExec\config\ .\game\config\
rem Shaderpacks
copy /Y .\MoonMCExec\shaderpacks\ .\game\shaderpacks\
echo Final setting...
del /f /s /q .\game\version.txt
copy /Y .\MoonMCExec\version.txt .\game\
rmdir /s /q .\MoonMCExec\
echo Success!
goto success
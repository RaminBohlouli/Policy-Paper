@echo off
cd /d %~dp0
git add .
set /p commitMessage=Enter commit message: 
git commit -m "%commitMessage%"
git push
pause
@echo off
REM 啟動 Anaconda 虛擬環境並切換資料夾

call %USERPROFILE%\anaconda3\Scripts\activate.bat
call conda activate 104project
cd /d "C:\Users\FM_pc\Desktop\jobs_analysis_project"

code .


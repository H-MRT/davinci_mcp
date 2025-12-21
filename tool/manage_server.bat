@echo off
chcp 65001 >nul 2>&1
:menu
cls
echo ======================================
echo  サーバー管理メニュー (ポート8000)
echo ======================================
echo.
echo  1. check state
echo  2. stop
echo  3. exit
echo.
echo ======================================
set /p choice=選択してください (1-3): 

if "%choice%"=="1" goto check
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto end
echo.
echo 無効な選択です。1-3の数字を入力してください。
timeout /t 2 >nul
goto menu

:check
echo.
echo ======================================
echo サーバー状態確認中...
echo ======================================
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "$connections = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; if ($connections) { $connections | Select-Object LocalAddress, LocalPort, State, OwningProcess | Format-Table -AutoSize; Write-Host ''; Write-Host 'サーバーが起動しています' -ForegroundColor Green } else { Write-Host 'ポート8000でリッスンしているサーバーは見つかりませんでした' -ForegroundColor Yellow }"
echo.
pause
goto menu

:stop
echo.
echo ======================================
echo サーバー停止処理中...
echo ======================================
echo.
powershell -Command ^
"$connections = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; ^
if ($connections) { ^
  $processId = $connections.OwningProcess; ^
  Write-Host \"プロセスID: $processId を停止します...\" -ForegroundColor Yellow; ^
  Stop-Process -Id $processId -Force; ^
  Start-Sleep -Seconds 1; ^
  $check = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; ^
  if (-not $NoProfile -ExecutionPolicy Bypass -Command "$connections = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; if ($connections) { $processId = $connections.OwningProcess; Write-Host \"プロセスID: $processId を停止します...\" -ForegroundColor Yellow; Stop-Process -Id $processId -Force; Start-Sleep -Seconds 1; $check = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; if (-not $check) { Write-Host \"サーバーを正常に停止しました\" -ForegroundColor Green } else { Write-Host \"サーバーの停止に失敗しました\" -ForegroundColor Red } } else { Write-Host 'ポート8000でリッスンしているサーバーは見つかりませんでした' -ForegroundColor Yellow timeout /t 1 >nul
exit

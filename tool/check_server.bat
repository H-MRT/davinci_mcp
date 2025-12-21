@echo off
chcp 65001 >nul
echo ======================================
echo ポート8000のサーバー状態確認
echo ======================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "$connections = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; if ($connections) { $connections | Select-Object LocalAddress, LocalPort, State, OwningProcess | Format-Table -AutoSize; Write-Host ''; Write-Host 'サーバーが起動しています' -ForegroundColor Green } else { Write-Host 'ポート8000でリッスンしているサーバーは見つかりませんでした' -ForegroundColor Yellow }"

echo.
pause

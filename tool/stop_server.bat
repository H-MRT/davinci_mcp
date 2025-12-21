@echo off
chcp 65001 >nul
echo ======================================
echo ポート8000のサーバー停止
echo ======================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command "$connections = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; if ($connections) { $processId = $connections.OwningProcess; Write-Host \"プロセスID: $processId を停止します...\" -ForegroundColor Yellow; Stop-Process -Id $processId -Force; Start-Sleep -Seconds 1; $check = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue; if (-not $check) { Write-Host \"サーバーを正常に停止しました\" -ForegroundColor Green } else { Write-Host \"サーバーの停止に失敗しました\" -ForegroundColor Red } } else { Write-Host 'ポート8000でリッスンしているサーバーは見つかりませんでした' -ForegroundColor Yellow }"

echo.
pause

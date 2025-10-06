# MedAdhere - Start All Servers
# This script starts both backend and frontend servers

Write-Host "🚀 Starting MedAdhere Application..." -ForegroundColor Cyan
Write-Host ""

$projectPath = "c:\Users\ab\Downloads\AI-Powered Dynamic Pricing Engine"

# Check if we're in the right directory
if (!(Test-Path "$projectPath\src")) {
    Write-Host "❌ Error: Cannot find project files!" -ForegroundColor Red
    Write-Host "   Expected location: $projectPath" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "📂 Project found at: $projectPath" -ForegroundColor Green
Write-Host ""

# Start Backend
Write-Host "🔵 Starting Backend Server (Port 8010)..." -ForegroundColor Cyan
$backendJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    & "$path\.venv\Scripts\python.exe" -m uvicorn src.api.main:app --reload --port 8010
} -ArgumentList $projectPath

Start-Sleep -Seconds 3

# Check if backend started
$backendRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8010/health" -Method Get -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend is running on http://localhost:8010" -ForegroundColor Green
        $backendRunning = $true
    }
} catch {
    Write-Host "⏳ Backend starting up..." -ForegroundColor Yellow
}

Write-Host ""

# Start Frontend
Write-Host "🟢 Starting Frontend Server (Port 3008)..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    node frontend/server.js
} -ArgumentList $projectPath

Start-Sleep -Seconds 2

# Check if frontend started
$frontendRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3008" -Method Get -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend is running on http://localhost:3008" -ForegroundColor Green
        $frontendRunning = $true
    }
} catch {
    Write-Host "⏳ Frontend starting up..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  MedAdhere is starting!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Frontend:  http://localhost:3008" -ForegroundColor White
Write-Host "🔌 Backend:   http://localhost:8010" -ForegroundColor White
Write-Host "📚 API Docs:  http://localhost:8010/docs" -ForegroundColor White
Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Wait a bit more for services to fully start
Write-Host "⏳ Waiting for services to fully start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Final verification
Write-Host ""
Write-Host "🔍 Verifying services..." -ForegroundColor Cyan

# Check backend
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8010/health" -Method Get -TimeoutSec 5
    Write-Host "✅ Backend: HEALTHY" -ForegroundColor Green
    Write-Host "   $($response | ConvertTo-Json -Compress)" -ForegroundColor DarkGray
} catch {
    Write-Host "⚠️  Backend: Still starting (give it a few more seconds)" -ForegroundColor Yellow
}

# Check frontend
try {
    Invoke-WebRequest -Uri "http://localhost:3008" -Method Get -TimeoutSec 5 | Out-Null
    Write-Host "✅ Frontend: RUNNING" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Frontend: Still starting (give it a few more seconds)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🎉 Ready! Opening browser..." -ForegroundColor Green
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Open browser
Start-Sleep -Seconds 2
Start-Process "http://localhost:3008"

Write-Host ""
Write-Host "🛑 To stop servers, close this window or press Ctrl+C" -ForegroundColor Yellow
Write-Host ""
Write-Host "📊 Watching for changes..." -ForegroundColor Cyan
Write-Host ""

# Keep script running and show job status
try {
    while ($true) {
        Start-Sleep -Seconds 10
        
        # Check if jobs are still running
        $backendState = (Get-Job -Id $backendJob.Id).State
        $frontendState = (Get-Job -Id $frontendJob.Id).State
        
        if ($backendState -ne "Running") {
            Write-Host "⚠️  Backend stopped unexpectedly!" -ForegroundColor Red
            Write-Host "   Checking error..." -ForegroundColor Yellow
            Receive-Job -Id $backendJob.Id
            break
        }
        
        if ($frontendState -ne "Running") {
            Write-Host "⚠️  Frontend stopped unexpectedly!" -ForegroundColor Red
            Write-Host "   Checking error..." -ForegroundColor Yellow
            Receive-Job -Id $frontendJob.Id
            break
        }
    }
} finally {
    Write-Host ""
    Write-Host "🛑 Stopping servers..." -ForegroundColor Yellow
    Stop-Job -Id $backendJob.Id -ErrorAction SilentlyContinue
    Stop-Job -Id $frontendJob.Id -ErrorAction SilentlyContinue
    Remove-Job -Id $backendJob.Id -ErrorAction SilentlyContinue
    Remove-Job -Id $frontendJob.Id -ErrorAction SilentlyContinue
    Write-Host "✅ All servers stopped" -ForegroundColor Green
}

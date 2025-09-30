# MedAdhere Startup Script
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "     MedAdhere - AI Medication System      " -ForegroundColor Cyan  
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Set the project directory
$projectDir = "c:\Users\ab\Downloads\AI-Powered Dynamic Pricing Engine"
$pythonPath = "C:/Users/ab/AppData/Local/Programs/Python/Python313/python.exe"

Write-Host "Starting MedAdhere Backend Server..." -ForegroundColor Green
Set-Location $projectDir
Start-Process -FilePath "cmd" -ArgumentList "/k", "$pythonPath main.py" -WindowStyle Normal

Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Starting MedAdhere Frontend Server..." -ForegroundColor Green
Set-Location "$projectDir\frontend"
Start-Process -FilePath "cmd" -ArgumentList "/k", "$pythonPath -m http.server 3000" -WindowStyle Normal

Write-Host "Waiting for frontend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host "         MedAdhere is now running!         " -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access your application:" -ForegroundColor White
Write-Host "  Desktop Web App: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Mobile Web App:  " -NoNewline -ForegroundColor White  
Write-Host "http://localhost:3000/mobile.html" -ForegroundColor Cyan
Write-Host "  API Documentation: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

Write-Host "Opening web browser..." -ForegroundColor Yellow
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "Press any key to exit (servers will keep running)..." -ForegroundColor White
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
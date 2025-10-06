# Azure Deployment Status Checker
$RESOURCE_GROUP = "med"
$APP_NAME = "medadhere-backend"
$APP_URL = "https://$APP_NAME.azurewebsites.net"

Write-Host "🔍 Checking Azure Deployment Status..." -ForegroundColor Cyan
Write-Host ""

# Test health endpoint directly
Write-Host "🏥 Testing backend health..." -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri "$APP_URL/health" -Method Get -TimeoutSec 10 -ErrorAction Stop
    Write-Host "✅ Backend is HEALTHY!" -ForegroundColor Green
    Write-Host "   Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor White
    Write-Host ""
    Write-Host "🎉 Deployment Successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📚 API Documentation: $APP_URL/docs" -ForegroundColor Cyan
    Write-Host "🌐 Health Check: $APP_URL/health" -ForegroundColor Cyan
    Write-Host ""
    
    Start-Process "$APP_URL/docs"
    
} catch {
    Write-Host "❌ Backend not responding yet" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔄 Deployment is still in progress..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📊 Monitor deployment here:" -ForegroundColor Cyan
    Write-Host "   GitHub Actions: https://github.com/MuhammadSaif700/Medadhere/actions" -ForegroundColor White
    Write-Host ""
    Write-Host "⏱️ Expected time: 7-11 minutes from last push" -ForegroundColor Yellow
    Write-Host ""
    
    Start-Process "https://github.com/MuhammadSaif700/Medadhere/actions"
}

Write-Host ""


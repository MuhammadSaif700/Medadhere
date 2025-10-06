# Azure Deployment Status Checker
# Run this script to monitor your deployment

$RESOURCE_GROUP = "med"
$APP_NAME = "medadhere-backend"
$APP_URL = "https://$APP_NAME.azurewebsites.net"

Write-Host "🔍 Checking Azure Deployment Status..." -ForegroundColor Cyan
Write-Host ""

# Check if Azure CLI is installed
if (!(Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Azure CLI not installed" -ForegroundColor Red
    Write-Host "📥 Install from: https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📊 Check deployment manually:" -ForegroundColor Yellow
    Write-Host "   1. GitHub Actions: https://github.com/MuhammadSaif700/Medadhere/actions" -ForegroundColor White
    Write-Host "   2. Azure Portal: https://portal.azure.com" -ForegroundColor White
    exit
}

Write-Host "✅ Azure CLI found" -ForegroundColor Green
Write-Host ""

# Try to get app status
Write-Host "📱 Checking Web App status..." -ForegroundColor Cyan
try {
    $status = az webapp show --resource-group $RESOURCE_GROUP --name $APP_NAME --query "state" --output tsv 2>$null
    
    if ($status -eq "Running") {
        Write-Host "✅ Web App is Running!" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Web App Status: $status" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Could not check app status (might not exist yet)" -ForegroundColor Yellow
}

Write-Host ""

# Test health endpoint
Write-Host "🏥 Testing health endpoint..." -ForegroundColor Cyan
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
    
    # Open API docs
    $openDocs = Read-Host "Open API docs in browser? (y/n)"
    if ($openDocs -eq 'y') {
        Start-Process "$APP_URL/docs"
    }
    
} catch {
    Write-Host "❌ Backend not responding yet" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔄 Deployment might still be in progress..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📊 Check deployment progress:" -ForegroundColor Cyan
    Write-Host "   1. GitHub Actions: https://github.com/MuhammadSaif700/Medadhere/actions" -ForegroundColor White
    Write-Host "   2. Azure Portal → $APP_NAME → Deployment Center → Logs" -ForegroundColor White
    Write-Host ""
    Write-Host "⏱️ Expected time: 7-11 minutes" -ForegroundColor Yellow
    Write-Host ""
    
    # Open GitHub Actions
    $openGH = Read-Host "Open GitHub Actions to monitor deployment? (y/n)"
    if ($openGH -eq 'y') {
        Start-Process "https://github.com/MuhammadSaif700/Medadhere/actions"
    }
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

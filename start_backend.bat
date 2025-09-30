@echo off
echo =====================================================
echo        MedAdhere - Backend Server Startup
echo =====================================================
echo.
echo Starting MedAdhere Backend API Server...
echo Server will be available at: http://localhost:8007
echo API Documentation at: http://localhost:8007/docs
echo Health Check at: http://localhost:8007/health
echo.
cd /d "c:\Users\ab\Downloads\AI-Powered Dynamic Pricing Engine"
echo Initializing database and starting server...
"C:\Users\ab\AppData\Local\Programs\Python\Python313\python.exe" main.py
echo.
echo Server stopped. Press any key to close.
pause
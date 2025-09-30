@echo off
echo =====================================================
echo          MedAdhere - Complete Application
echo =====================================================
echo.
echo Starting MedAdhere AI Medication Adherence System...
echo.
echo This will start both Backend and Frontend servers:
echo  - Backend API: http://localhost:8000
echo  - Frontend Web: http://localhost:3000  
echo  - Mobile App: http://localhost:3000/mobile.html
echo  - API Docs: http://localhost:8000/docs
echo.
echo Starting Backend Server...
start "MedAdhere Backend" cmd /k "cd /d c:\Users\ab\Downloads\AI-Powered Dynamic Pricing Engine && C:/Users/ab/AppData/Local/Programs/Python/Python313/python.exe main.py"

echo Waiting 3 seconds for backend to initialize...
timeout /t 3 /nobreak

echo Starting Frontend Server...
start "MedAdhere Frontend" cmd /k "cd /d c:\Users\ab\Downloads\AI-Powered Dynamic Pricing Engine\frontend && C:/Users/ab/AppData/Local/Programs/Python/Python313/python.exe -m http.server 3000"

echo Waiting 2 seconds for frontend to start...
timeout /t 2 /nobreak

echo.
echo =====================================================
echo           MedAdhere is now running!
echo =====================================================
echo.
echo Access your application:
echo  Desktop Web App: http://localhost:3000
echo  Mobile Web App:  http://localhost:3000/mobile.html
echo  API Documentation: http://localhost:8000/docs
echo.
echo Opening web browser...
start http://localhost:3000

echo.
echo Press any key to close this window (servers will keep running)
pause
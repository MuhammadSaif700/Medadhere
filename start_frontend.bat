@echo off
echo =====================================================
echo        MedAdhere - Frontend Server Startup  
echo =====================================================
echo.
echo Starting MedAdhere Web Interface...
echo Desktop App: http://localhost:3007
echo Mobile App: http://localhost:3007/mobile.html
echo.
cd /d "c:\Users\ab\Downloads\AI-Powered Dynamic Pricing Engine\frontend"
echo Starting Node.js HTTP server...
node -e "const http=require('http'),fs=require('fs'),path=require('path'); http.createServer((req,res)=>{let f=path.join(__dirname,req.url==='/'?'index.html':req.url); fs.readFile(f,(e,c)=>{if(e){res.writeHead(404);res.end('Not found');return;} let t='text/html'; if(f.endsWith('.js'))t='application/javascript'; if(f.endsWith('.css'))t='text/css'; res.writeHead(200,{'Content-Type':t,'Access-Control-Allow-Origin':'*'}); res.end(c);});}).listen(3007,()=>console.log('MedAdhere Frontend ready at http://localhost:3007'));"
echo.
echo Server stopped. Press any key to close.
pause
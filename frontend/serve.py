#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple HTTP server to serve MedAdhere frontend files.
Serves both desktop (index.html) and mobile (mobile.html) versions.
"""

import os
import sys
import http.server
import socketserver
import webbrowser
from pathlib import Path

class MedAdhereHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for MedAdhere frontend."""
    
    def end_headers(self):
        # Add CORS headers for API requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Handle root path
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/mobile':
            self.path = '/mobile.html'
        
        return super().do_GET()

def main():
    """Start the MedAdhere frontend server."""
    # Get the frontend directory
    frontend_dir = Path(__file__).parent
    os.chdir(frontend_dir)
    
    port = 3000
    
    # Find available port
    while port < 3010:
        try:
            with socketserver.TCPServer(("", port), MedAdhereHTTPRequestHandler) as httpd:
                print("\nMedAdhere Frontend Server")
                print("Mobile version: http://localhost:{}/mobile".format(port))
                print("Desktop version: http://localhost:{}/".format(port))
                print("Backend API: http://localhost:8000")
                print("\nServing from: {}".format(frontend_dir))
                print("Press Ctrl+C to stop the server")
                
                # Auto-open browser
                try:
                    webbrowser.open('http://localhost:{}/'.format(port))
                except:
                    pass
                
                httpd.serve_forever()
        except OSError:
            port += 1
            continue
        break
    else:
        print("Could not find an available port between 3000-3009")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print("Error starting server: {}".format(e))
        sys.exit(1)
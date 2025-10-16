#!/usr/bin/env python3
"""
Simple HTTP Server for Western Balkans Dashboard
Starts a local web server on port 8080 to serve the dashboard files.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def start_dashboard_server(port=8080):
    """Start the dashboard server on the specified port."""
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Create the server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print("=" * 60)
            print("🌍 Western Balkans Dashboard Server")
            print("=" * 60)
            print(f"📡 Server running on: http://localhost:{port}")
            print(f"📁 Serving files from: {project_dir}")
            print("=" * 60)
            print("🚀 Opening dashboard in your browser...")
            print("=" * 60)
            print("💡 To stop the server, press Ctrl+C")
            print("=" * 60)
            
            # Open the dashboard in the default browser
            webbrowser.open(f'http://localhost:{port}')
            
            # Start serving
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Error: Port {port} is already in use.")
            print(f"💡 Try a different port or stop the existing server.")
            print(f"💡 You can also try: python -m http.server {port + 1}")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    # Check if a custom port is provided
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Error: Port must be a number")
            print("💡 Usage: python start_server.py [port]")
            sys.exit(1)
    
    start_dashboard_server(port)

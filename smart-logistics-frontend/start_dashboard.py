#!/usr/bin/env python3
"""
Launcher for Smart Logistics Dashboard
"""
import subprocess
import sys
import webbrowser
import time
import os

def main():
    """Launch the Streamlit dashboard"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_path = os.path.join(script_dir, "simple_dashboard.py")
    
    print("🚚 Starting Smart Logistics AI Dashboard...")
    print(f"📁 Dashboard location: {dashboard_path}")
    print("🌐 Starting Streamlit server...")
    
    try:
        # Start streamlit server
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            dashboard_path,
            "--server.headless", "true",
            "--server.port", "8501"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Open browser
        webbrowser.open("http://localhost:8501")
        print("🌐 Dashboard opened in browser: http://localhost:8501")
        print("🔄 Press Ctrl+C to stop the server")
        
        # Wait for process
        process.wait()
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

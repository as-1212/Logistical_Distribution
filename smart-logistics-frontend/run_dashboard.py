#!/usr/bin/env python3
"""
Simple runner for the Smart Logistics Dashboard
"""
import subprocess
import sys
import os

def main():
    """Run the Streamlit dashboard"""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_path = os.path.join(script_dir, "dashboard.py")
    
    print("🚚 Starting Smart Logistics AI Dashboard...")
    print(f"📁 Dashboard location: {dashboard_path}")
    print("🌐 Opening in browser...")
    
    try:
        # Run streamlit using python -m
        subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running dashboard: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()

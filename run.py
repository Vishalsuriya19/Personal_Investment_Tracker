#!/usr/bin/env python3
"""
Run Investment Tracker Application
This script starts all required services in separate processes
"""

import subprocess
import os
import sys
import time
from pathlib import Path

def run_command(cmd, name):
    """Run a command in a new terminal"""
    print(f"Starting {name}...")
    
    if sys.platform == 'win32':
        # Windows
        subprocess.Popen(
            ['cmd', '/k', cmd],
            cwd=os.getcwd()
        )
    else:
        # macOS/Linux
        subprocess.Popen(
            ['gnome-terminal', '--', 'bash', '-c', cmd],
            cwd=os.getcwd()
        )
    
    time.sleep(2)

def main():
    """Start all services"""
    print("""
╔═══════════════════════════════════════╗
║   AI Personal Investment Tracker      ║
║          Application Launcher         ║
╚═══════════════════════════════════════╝
    """)
    
    # Check if virtual environment is activated
    if sys.prefix == sys.base_prefix:
        print("⚠️  Virtual environment is not activated!")
        print("Please run: venv\\Scripts\\activate.bat (Windows)")
        print("            source venv/bin/activate (macOS/Linux)")
        return
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("❌ .env file not found. Please copy .env.example to .env")
        return
    
    # Train ML models
    print("\n[1/4] Training ML models...")
    try:
        subprocess.run(
            [sys.executable, 'ml_models/train_model.py'],
            check=True,
            capture_output=False
        )
        print("✓ ML models trained")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error training models: {e}")
        return
    
    print("\n" + "="*50)
    print("🚀 Starting all services...")
    print("="*50 + "\n")
    
    # Start Flask Backend
    if sys.platform == 'win32':
        run_command(
            f'{sys.executable} backend/app.py',
            'Flask Backend'
        )
    else:
        run_command(
            f'{sys.executable} backend/app.py',
            'Flask Backend'
        )
    
    # Start Streamlit Frontend
    time.sleep(3)
    if sys.platform == 'win32':
        run_command(
            f'streamlit run frontend/app.py',
            'Streamlit Frontend'
        )
    else:
        run_command(
            f'streamlit run frontend/app.py',
            'Streamlit Frontend'
        )
    
    print("\n" + "="*50)
    print("✓ All services started!")
    print("="*50)
    print("""
Services running:
  🔧 API Backend: http://localhost:5000
  🖥️  Frontend UI: http://localhost:8501
  
Press Ctrl+C in any terminal to stop services.
    """)
    
    # Keep script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down services...")

if __name__ == '__main__':
    main()

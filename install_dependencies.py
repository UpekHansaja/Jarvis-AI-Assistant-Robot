#!/usr/bin/env python3
"""
Installation script for JARVIS AI Assistant
This will install all required dependencies
"""

import sys
import subprocess
import platform

def check_python_version():
    """Check if Python is version 3.6 or higher"""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version}")

def install_packages():
    """Install required packages using pip"""
    packages = [
        "pyserial",
        "pyttsx3",
        "SpeechRecognition",
        "pywhatkit",
        "requests",
        "PyAudio"
    ]
    
    print("\n📦 Installing required packages...")
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            
            if package == "PyAudio" and platform.system() == "Darwin":  # macOS
                print("\n🛠️  PyAudio installation failed. On macOS, try:")
                print("brew install portaudio")
                print("pip install PyAudio")
            
            if package == "pywhatkit":
                print("\n🛠️  For pywhatkit, you may need to install:")
                print("pip install wikipedia")
                print("pip install Pillow")

def setup_instructions():
    """Print setup instructions"""
    print("\n" + "="*60)
    print("JARVIS AI Assistant - Setup Instructions")
    print("="*60)
    print("\n1. Make sure your Arduino is connected")
    print("2. Upload the correct Arduino sketch to your board")
    print("3. Test hardware with: python test_led_expressions.py")
    print("4. Test audio with: python test_mac_audio.py")
    print("5. Run JARVIS with: python main.py")
    print("\nMake sure your Mac's microphone permissions are enabled for Terminal/VS Code")
    print("="*60)

if __name__ == "__main__":
    print("="*60)
    print("JARVIS AI Assistant - Dependency Installation")
    print("="*60)
    
    check_python_version()
    install_packages()
    setup_instructions()

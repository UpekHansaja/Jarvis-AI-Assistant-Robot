#!/usr/bin/env python3
"""
Test script to verify voice output methods on macOS
Run this script to test different voice output methods
"""

import os
import time
import subprocess
import pyttsx3

def test_voice_methods(test_phrase="Hello, this is a voice output test for Jarvis assistant."):
    """Test various voice output methods on macOS"""
    print("\n" + "=" * 60)
    print("VOICE OUTPUT TEST SCRIPT")
    print("=" * 60)
    
    print("\nTesting different voice output methods with phrase:")
    print(f"  \"{test_phrase}\"")
    
    # Method 1: Basic OS system command
    print("\n" + "-" * 40)
    print("METHOD 1: Basic 'say' command")
    try:
        print("Executing: os.system('say \"" + test_phrase + "\"')")
        os.system(f'say "{test_phrase}"')
        print("✓ Basic say command completed")
        input("Press Enter to continue to next method...")
    except Exception as e:
        print(f"✗ Basic say command failed: {e}")
    
    # Method 2: OS system command with specific voice
    print("\n" + "-" * 40)
    print("METHOD 2: 'say' command with specific voice")
    try:
        print("Executing: os.system('say -v Samantha \"" + test_phrase + "\"')")
        os.system(f'say -v Samantha "{test_phrase}"')
        print("✓ Voice-specific say command completed")
        input("Press Enter to continue to next method...")
    except Exception as e:
        print(f"✗ Voice-specific say command failed: {e}")
    
    # Method 3: Subprocess command
    print("\n" + "-" * 40)
    print("METHOD 3: subprocess with 'say' command")
    try:
        print("Executing: subprocess.run(['say', '-v', 'Samantha', '" + test_phrase + "'])")
        subprocess.run(["say", "-v", "Samantha", test_phrase], check=True)
        print("✓ Subprocess say command completed")
        input("Press Enter to continue to next method...")
    except Exception as e:
        print(f"✗ Subprocess say command failed: {e}")
    
    # Method 4: pyttsx3 library
    print("\n" + "-" * 40)
    print("METHOD 4: pyttsx3 library")
    try:
        print("Initializing pyttsx3 engine...")
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"Found {len(voices)} voices")
        
        # Try to set a female voice
        female_found = False
        for voice in voices:
            if any(name in voice.id.lower() for name in ["samantha", "siri", "karen", "moira", "female"]):
                print(f"Setting voice to {voice.name} ({voice.id})")
                engine.setProperty('voice', voice.id)
                female_found = True
                break
        
        if not female_found:
            print("No female voice found, using default voice")
        
        # Set properties
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        
        print("Speaking with pyttsx3...")
        engine.say(test_phrase)
        engine.runAndWait()
        engine.stop()
        print("✓ pyttsx3 speech completed")
    except Exception as e:
        print(f"✗ pyttsx3 failed: {e}")
    
    print("\n" + "=" * 60)
    print("VOICE OUTPUT TEST COMPLETE")
    print("=" * 60)
    print("\nResults summary:")
    print("If you heard voice output from any method, we can use that method in Jarvis.")
    print("The most reliable method will be used in the main application.")

if __name__ == "__main__":
    test_voice_methods()

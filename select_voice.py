#!/usr/bin/env python3
"""
Voice Selection Tool for Jarvis AI Assistant
This tool helps you select and test different voices available on your Mac
and saves your preference for use with Jarvis
"""

import pyttsx3
import os
import time
import json
import sys

def list_available_voices():
    """List all available voices on the system"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print("\n" + "=" * 60)
    print("AVAILABLE VOICES")
    print("=" * 60)
    
    for i, voice in enumerate(voices):
        print(f"{i+1}. {voice.name}")
        print(f"   ID: {voice.id}")
        print(f"   Gender: {'Female' if 'female' in voice.name.lower() else 'Male'}")
        print(f"   Languages: {voice.languages}")
        print(f"   Age: {voice.age}")
        print("-" * 40)
    
    return voices

def test_voice(voice_id):
    """Test a specific voice by ID"""
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', 170)
    
    print(f"\nTesting voice: {voice_id}")
    
    test_phrases = [
        "Hello, I am Jarvis, your personal assistant.",
        "I can help you with daily tasks and answer your questions.",
        "How is this voice? Does it sound good?",
        "This is what I'll sound like if you select this voice."
    ]
    
    for phrase in test_phrases:
        print(f"Speaking: {phrase}")
        engine.say(phrase)
        engine.runAndWait()
        time.sleep(0.5)

def save_voice_preference(voice_id):
    """Save the selected voice ID to a configuration file"""
    config = {
        "voice_id": voice_id,
        "rate": 170,
        "volume": 1.0
    }
    
    with open("jarvis_voice_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\nVoice preference saved: {voice_id}")
    print(f"Config file: {os.path.abspath('jarvis_voice_config.json')}")

def test_system_voices():
    """Test macOS built-in voices using the 'say' command"""
    print("\n" + "=" * 60)
    print("TESTING MACOS SYSTEM VOICES")
    print("=" * 60)
    
    # Get list of voices from macOS
    os.system('say -v "?"')
    
    # Test some common female voices
    female_voices = ["Samantha", "Siri", "Karen", "Moira", "Tessa", "Fiona"]
    
    print("\nTesting common female voices:")
    for voice in female_voices:
        print(f"\nTesting: {voice}")
        os.system(f'say -v "{voice}" "Hello, I am {voice}. I could be your Jarvis assistant voice."')
        time.sleep(1)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("JARVIS VOICE SELECTION TOOL")
    print("=" * 60)
    
    print("\n1. This tool will help you select the best voice for Jarvis")
    print("2. You'll hear sample speech from available voices")
    print("3. Your selection will be saved for use with Jarvis\n")
    
    # List voices from pyttsx3
    voices = list_available_voices()
    
    # Also test system voices on macOS
    test_system_voices()
    
    # Let the user select a voice
    try:
        selection = input("\nEnter the number of the voice you want to use (or 'q' to quit): ")
        
        if selection.lower() == 'q':
            print("Exiting without saving preference.")
            sys.exit(0)
        
        voice_index = int(selection) - 1
        if 0 <= voice_index < len(voices):
            selected_voice = voices[voice_index]
            print(f"\nYou selected: {selected_voice.name}")
            
            # Test the selected voice
            test_voice(selected_voice.id)
            
            confirm = input("\nUse this voice for Jarvis? (y/n): ")
            if confirm.lower() == 'y':
                save_voice_preference(selected_voice.id)
                print("\nVoice preference saved! Jarvis will now use this voice.")
            else:
                print("\nVoice not saved. Run this tool again to select a different voice.")
        else:
            print("Invalid selection!")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try again.")
    
    print("\n" + "=" * 60)
    print("Thank you for using the Jarvis Voice Selection Tool!")
    print("=" * 60)

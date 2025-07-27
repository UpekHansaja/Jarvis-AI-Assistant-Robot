#!/usr/bin/env python3
"""
Voice Test and Selection Tool for Jarvis Assistant
This script helps users test and select the best voice for their system.
It will test both pyttsx3 voices and macOS system voices.
"""

import pyttsx3
import os
import subprocess
import sys
import time

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"{text:^60}")
    print("=" * 60 + "\n")

def test_pyttsx3_voices():
    """Test all available pyttsx3 voices"""
    print_header("Testing pyttsx3 Voices")
    
    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if not voices:
            print("No pyttsx3 voices found on your system.")
            return []
        
        print(f"Found {len(voices)} pyttsx3 voices:\n")
        
        voice_list = []
        for i, voice in enumerate(voices):
            voice_id = voice.id
            voice_name = voice.name if hasattr(voice, 'name') else voice_id.split('.')[-1]
            gender = "Female" if any(female_term in voice_id.lower() for female_term in ['female', 'woman', 'girl', 'karen', 'samantha', 'siri', 'moira']) else "Male"
            
            print(f"{i+1}. {voice_name} ({gender}) - ID: {voice_id}")
            voice_list.append({
                'index': i+1,
                'id': voice_id,
                'name': voice_name,
                'gender': gender,
                'type': 'pyttsx3'
            })
        
        return voice_list
    
    except Exception as e:
        print(f"Error testing pyttsx3 voices: {e}")
        return []

def test_macos_voices():
    """Test all available macOS system voices"""
    print_header("Testing macOS System Voices")
    
    try:
        # Get list of macOS voices
        result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Failed to get macOS voices.")
            return []
        
        voice_lines = result.stdout.strip().split('\n')
        
        if not voice_lines:
            print("No macOS voices found on your system.")
            return []
        
        print(f"Found {len(voice_lines)} macOS voices:\n")
        
        voice_list = []
        for i, line in enumerate(voice_lines):
            parts = line.split()
            if not parts:
                continue
            
            voice_name = parts[0]
            language = parts[-1].strip('()')
            gender = "Female" if any(female_term in line.lower() for female_term in ['female', 'woman', 'girl', 'karen', 'samantha', 'siri', 'moira']) else "Male"
            
            print(f"{i+1}. {voice_name} - {language} ({gender})")
            voice_list.append({
                'index': i+1,
                'id': voice_name,
                'language': language,
                'gender': gender,
                'type': 'macos'
            })
        
        return voice_list
    
    except Exception as e:
        print(f"Error testing macOS voices: {e}")
        return []

def test_voice(voice_info):
    """Test a specific voice"""
    print(f"\nTesting voice: {voice_info['name'] if 'name' in voice_info else voice_info['id']}")
    
    test_phrase = "Hello, I am Jarvis, your personal assistant. How may I help you today?"
    
    try:
        if voice_info['type'] == 'pyttsx3':
            engine = pyttsx3.init()
            engine.setProperty('voice', voice_info['id'])
            engine.setProperty('rate', 165)  # Slightly slower for clarity
            engine.setProperty('volume', 1.0)  # Full volume
            
            print("Speaking with pyttsx3...")
            engine.say(test_phrase)
            engine.runAndWait()
        
        elif voice_info['type'] == 'macos':
            print("Speaking with macOS say command...")
            os.system(f'say -v "{voice_info["id"]}" "{test_phrase}"')
        
    except Exception as e:
        print(f"Error testing voice: {e}")

def get_user_selection(voice_list):
    """Get user selection of preferred voice"""
    if not voice_list:
        return None
    
    while True:
        try:
            selection = input("\nEnter the number of the voice you want to test, or 'q' to quit: ")
            
            if selection.lower() == 'q':
                return None
            
            index = int(selection)
            for voice in voice_list:
                if voice['index'] == index:
                    return voice
            
            print("Invalid selection. Please try again.")
        
        except ValueError:
            print("Please enter a valid number.")

def save_voice_preference(voice_info):
    """Save the selected voice preference to a config file"""
    if not voice_info:
        return
    
    config_path = os.path.join(os.path.dirname(__file__), 'voice_config.py')
    
    with open(config_path, 'w') as f:
        f.write(f"""# Voice configuration for Jarvis Assistant
# Generated by test_and_select_voice.py

VOICE_TYPE = "{voice_info['type']}"
VOICE_ID = "{voice_info['id']}"
VOICE_NAME = "{voice_info.get('name', voice_info['id'])}"
VOICE_GENDER = "{voice_info.get('gender', 'Unknown')}"
VOICE_RATE = 165  # Speaking rate (words per minute)
VOICE_VOLUME = 1.0  # Volume (0.0 to 1.0)
""")
    
    print(f"\nVoice preference saved to {config_path}")
    print("Restart your Jarvis assistant to use the new voice settings.")

def main():
    print_header("Jarvis Voice Selection Tool")
    print("This tool will help you select the best voice for your Jarvis assistant.")
    
    combined_voices = []
    
    # Test pyttsx3 voices
    pyttsx3_voices = test_pyttsx3_voices()
    combined_voices.extend(pyttsx3_voices)
    
    # Test macOS voices
    macos_voices = test_macos_voices()
    combined_voices.extend(macos_voices)
    
    if not combined_voices:
        print("\nNo voices found on your system. Please check your installation.")
        return
    
    # Interactive voice testing
    print_header("Interactive Voice Testing")
    print("Now you can test individual voices and select your preferred one.")
    
    while True:
        voice = get_user_selection(combined_voices)
        
        if not voice:
            break
        
        test_voice(voice)
        
        save = input("\nDo you want to use this voice for Jarvis? (y/n): ")
        if save.lower() == 'y':
            save_voice_preference(voice)
            break

    print("\nThank you for using the Jarvis Voice Selection Tool.")

if __name__ == "__main__":
    main()

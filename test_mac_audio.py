#!/usr/bin/env python3
"""
Test script for Mac's microphone and speaker settings
Run this to verify your Mac's audio setup for Jarvis
"""

import speech_recognition as sr
import pyttsx3
import time
import os

def test_microphone():
    """Test if the default microphone is working"""
    print("\n===== TESTING MICROPHONE =====")
    recognizer = sr.Recognizer()
    
    # List available microphones
    print("\nAvailable microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  {index}: {name}")
    
    try:
        with sr.Microphone() as source:
            print("\n🎤 Adjusting for ambient noise... Please be quiet for a moment.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Ambient noise level adjusted.")
            
            print("\n🎤 Please say something...")
            audio = recognizer.listen(source, timeout=5)
            
            print("🔍 Processing speech...")
            try:
                text = recognizer.recognize_google(audio)
                print(f"✅ Recognized: '{text}'")
                return text
            except sr.UnknownValueError:
                print("❌ Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"❌ Could not request results from Google Speech Recognition service; {e}")
    
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
    
    return None

def test_speaker():
    """Test if the default speaker is working"""
    print("\n===== TESTING SPEAKER =====")
    try:
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        print("\nAvailable voices:")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name} ({voice.id})")
        
        # Use current settings
        current_voice = engine.getProperty('voice')
        print(f"\nCurrently using voice: {current_voice}")
        
        # Test speaking
        print("\n🔊 Testing speaker... You should hear a voice.")
        engine.say("This is a test of your Mac's speaker system. If you can hear this, your speaker is working correctly.")
        engine.runAndWait()
        print("✅ Speaker test completed.")
        
        # Check if we should test other voices
        test_more = input("\nWould you like to test female voices? (y/n): ")
        if test_more.lower() == 'y':
            test_female_voices(engine, voices)
            
        return True
        
    except Exception as e:
        print(f"❌ Speaker test failed: {e}")
        # Try system say command as fallback
        try:
            print("Attempting to use system 'say' command as fallback...")
            os.system('say "This is a test using the Mac system voice command. If you can hear this, your speaker is working correctly."')
            print("✅ System voice command test completed.")
            return True
        except:
            print("❌ System voice command also failed.")
    
    return False

def test_female_voices(engine, voices):
    """Test female voices that would be suitable for Jarvis"""
    print("\n===== TESTING FEMALE VOICES =====")
    
    # Look for female voices
    female_voices = []
    for voice in voices:
        voice_id_lower = voice.id.lower()
        voice_name_lower = voice.name.lower()
        
        if any(name in voice_id_lower or name in voice_name_lower 
               for name in ["female", "samantha", "siri", "karen", "moira"]):
            female_voices.append(voice)
    
    if not female_voices:
        print("❌ No specific female voices found in your system.")
        print("Run the select_voice.py tool to check all available voices.")
        return
        
    print(f"\nFound {len(female_voices)} potential female voices:")
    
    # Test each female voice
    for i, voice in enumerate(female_voices):
        print(f"\n{i+1}. Testing: {voice.name}")
        engine.setProperty('voice', voice.id)
        engine.say(f"Hello, I am using the {voice.name} voice. I could be your Jarvis assistant.")
        engine.runAndWait()
        
    print("\n✅ Female voice test completed.")
    print("Run the select_voice.py tool to set your preferred voice for Jarvis.")

def echo_test():
    """Perform a mic-speaker loop test"""
    print("\n===== PERFORMING ECHO TEST =====")
    text = test_microphone()
    
    if text:
        print("\n🔄 Echoing what you said...")
        engine = pyttsx3.init()
        engine.say(f"I heard you say: {text}")
        engine.runAndWait()

if __name__ == "__main__":
    print("=" * 60)
    print("      MAC AUDIO SYSTEM TEST FOR JARVIS")
    print("=" * 60)
    
    test_speaker()
    time.sleep(1)
    echo_test()
    
    print("\n" + "=" * 60)
    print("      TEST COMPLETED")
    print("=" * 60)

# JARVIS AI Assistant

A voice-controlled personal assistant that responds to your commands and questions through LED expressions and voice feedback.

## Features

- Voice recognition with wake word "Jarvis"
- LED expressions to show different emotions
- Answers common daily questions:
  - Time and date
  - Weather information
  - Facts and jokes
  - General knowledge questions
- Can perform actions:
  - Search the web
  - Play YouTube videos
  - Open websites
  - Provide information

## Hardware Requirements

- Arduino Uno
- 5 LEDs in different colors:
  - Green (Happy) - Connected to pin 3
  - Blue (Sad) - Connected to pin 5
  - Yellow (Thinking) - Connected to pin 6
  - Red (Angry) - Connected to pin 9
  - White (Status) - Connected to pin 11
- Resistors (220Ω) for each LED
- Breadboard and jumper wires
- USB cable to connect Arduino to computer

## Software Requirements

- Python 3.6+
- Arduino IDE
- Required Python packages (install with `pip install`):
  - pyserial
  - pyttsx3
  - SpeechRecognition
  - pywhatkit
  - requests
  - PyAudio

## Quick Start Guide

1. **Install Dependencies**
   ```bash
   python install_dependencies.py
   ```

2. **Connect the Arduino**
   - Wire the LEDs according to the pin assignments
   - Connect Arduino to your computer via USB

3. **Upload Arduino Code**
   - Open `arduino_led_expressions.ino` in Arduino IDE
   - Select your board and port
   - Upload the code

4. **Test the Hardware**
   ```bash
   python test_led_expressions.py
   ```

5. **Test Audio System**
   ```bash
   python test_mac_audio.py
   ```

6. **Select a Female Voice (Similar to Siri)**
   ```bash
   python select_voice.py
   ```
   This tool lets you choose and test different female voices for Jarvis.
   
7. **Run Jarvis**
   ```bash
   python main.py
   ```

7. **Speak commands starting with "Jarvis"**
   - "Jarvis, what time is it?"
   - "Jarvis, what's the weather today?"
   - "Jarvis, tell me a joke"
   - "Jarvis, play some music"

## Troubleshooting

- **Microphone not working?**
  - Check system permissions for your Terminal or VS Code
  - Try running with elevated permissions
  
- **Arduino not connecting?**
  - Check the port in the code
  - Try unplugging and reconnecting
  - Verify the correct code is uploaded

- **Voice commands not recognized?**
  - Speak clearly and directly to the microphone
  - Try in a quieter environment
  - Check internet connection for speech recognition

## Voice Commands

| Command | Action |
|---------|--------|
| "Jarvis, what time is it?" | Tells the current time |
| "Jarvis, what's the date today?" | Tells the current date |
| "Jarvis, what's the weather?" | Provides weather information |
| "Jarvis, tell me a joke" | Tells a random joke |
| "Jarvis, tell me a fact" | Shares an interesting fact |
| "Jarvis, play [song name]" | Plays video on YouTube |
| "Jarvis, search for [query]" | Searches Google |
| "Jarvis, open [website]" | Opens website in browser |
| "Jarvis, what should I do today?" | Suggests an activity |
| "Jarvis, how are you?" | Responds with status |
| "Jarvis, help" | Lists available commands |

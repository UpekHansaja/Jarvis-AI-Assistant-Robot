""" JAUNDICE: AI Assistant robot with Arduino and Python

author: ashraf minhaj
mail: ashraf_minhaj@yahoo.com
Last Edit: Nov 2020

License: Copyright (C) Ashraf Minhaj.
General Public License (GPL3+)
"""


import speech_recognition as sr   # voice recognition library
import random                     # to choose random words from list
import pyttsx3                    # offline Text to Speech
import webbrowser                 # to open and perform web tasks
import serial                     # for serial communication
import pywhatkit                  # for more web automation
import time                       # for sleep and timing functions
import re                         # for regular expressions
import os                         # for os related operations
import platform                   # for system information
import subprocess                 # for running system commands
import requests                   # for API requests
import socket                     # for network information
import shutil                     # for disk usage information
import json                       # for handling JSON data
import psutil                     # for battery and system stats
import locale                     # for system locale settings
from urllib.parse import quote    # for URL encoding
from datetime import datetime, timezone, timedelta

# Global variables
voice_engine = None  # Global TTS engine that will be initialized at startup

# Declare robot name (Wake-Up word)
robot_name = 'jarvis'

# random words list
hi_words = ['hi', 'hello', 'yo boss', 'greetings']
bye_words = ['bye', 'goodbye', 'until next time']
r_u_there = ['are you there', 'you there']

# Initialize text to speech engine with Mac's system voice (female Siri-like)
def setup_voice():
    """Set up the text-to-speech engine with the preferred voice"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_voice_config.json")
    
    # Default voice settings
    rate = 170  # slightly slower for clarity
    volume = 1.0
    selected_voice = None
    
    # Try to load saved voice preference
    try:
        if os.path.exists(voice_config_file):
            with open(voice_config_file, 'r') as f:
                config = json.load(f)
                
            voice_id = config.get('voice_id')
            rate = config.get('rate', 170)
            volume = config.get('volume', 1.0)
            
            # Find the voice in available voices
            for voice in voices:
                if voice.id == voice_id:
                    selected_voice = voice
                    print(f"Using saved voice preference: {voice.name}")
                    break
    except Exception as e:
        print(f"Error loading voice config: {e}")
    
    # If no saved preference or it wasn't found, find a female voice
    if not selected_voice:
        print("No saved voice preference found, searching for a female voice...")
        
        # Print available voices for information
        print("Available voices:")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name} ({voice.id})")
        
        # First try macOS specific voices that sound like Siri
        female_names = ["samantha", "siri", "karen", "moira", "tessa", "fiona", "female", "woman", "girl"]
        
        # Look for voices with female names
        for voice in voices:
            voice_id_lower = voice.id.lower()
            voice_name_lower = voice.name.lower()
            
            if any(female_name in voice_id_lower or female_name in voice_name_lower for female_name in female_names):
                selected_voice = voice
                print(f"Selected female voice: {voice.name}")
                break
        
        # Fallback to any available voice
        if not selected_voice and voices:
            # Try to use second voice if available (often female in default setup)
            selected_voice = voices[1] if len(voices) > 1 else voices[0]
            print(f"Using fallback voice: {selected_voice.name}")
    
    # Set the voice properties
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    if selected_voice:
        engine.setProperty('voice', selected_voice.id)
    
    # Inform user how to change voice
    print(f"To select a different voice, run: python select_voice.py")
    
    return engine

# Set up the voice engine
try:
    print("Initializing voice engine...")
    engine = setup_voice()
    print("Voice engine setup complete")
except Exception as voice_error:
    print(f"Error setting up voice engine: {voice_error}")
    print("Attempting to use a basic voice engine setup")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
    except Exception as fallback_error:
        print(f"Fallback voice engine failed: {fallback_error}")
        engine = None

# Initialize speech recognition with Mac's default microphone
listener = sr.Recognizer()
listener.energy_threshold = 4000           # increase if too sensitive 
listener.dynamic_energy_threshold = True   # auto-adjust for ambient noise
listener.pause_threshold = 0.8             # seconds of non-speaking before phrase is complete

# connect with Arduino over serial communication
try:
    # Try common macOS serial ports
    import glob
    ports = glob.glob('/dev/tty.usbserial*') + glob.glob('/dev/tty.usbmodem*') + glob.glob('/dev/cu.usbserial*') + glob.glob('/dev/cu.usbmodem*')
    
    if ports:
        port = serial.Serial(ports[0], 9600, timeout=1)
        print(f"Physical body connected on {ports[0]}")
    else:
        # Fallback - try manual port specification
        port = serial.Serial("/dev/tty.usbmodem14101", 9600, timeout=1)  # Update this path as needed
        print("Physical body connected on fallback port")
except Exception as e:
    print(f"Unable to connect to my physical body: {e}")
    print("Available ports:", [p for p in glob.glob('/dev/tty.*') + glob.glob('/dev/cu.*') if 'usb' in p.lower()])
    port = None

# Utility functions for daily tasks
# Default location for weather - will be updated when get_location_info is called
default_location = "San Francisco"

def get_weather_info(city=""):
    """Get simple weather information using a public API"""
    try:
        from urllib.parse import quote
        
        # Use a free weather API that doesn't require a key
        if not city:
            # Use global default_location, which might have been updated by get_location_info
            global default_location
            city = default_location
        
        base_url = f"https://wttr.in/{quote(city)}?format=3"
        response = requests.get(base_url)
        
        if response.status_code == 200:
            weather_info = response.text
            # Add the city name if not already in the response
            if city.lower() not in weather_info.lower():
                weather_info = f"Weather in {city}: {weather_info}"
            return weather_info
        else:
            return f"I couldn't get the weather information for {city} right now."
    except Exception as e:
        print(f"Weather error: {e}")
        return "I'm having trouble getting weather data."

def get_time_info():
    """Get current time with formatted output"""
    now = datetime.now()
    hour = now.hour
    
    # Determine time of day greeting
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    time_str = now.strftime("%I:%M %p")
    return f"{greeting}. It's {time_str}."

def get_date_info():
    """Get current date with formatted output"""
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y")

def get_fact():
    """Return a random interesting fact"""
    facts = [
        "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion.",
        "20% of Earth's oxygen is produced by the Amazon rainforest.",
        "Honey never spoils. Archaeologists found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "A day on Venus is longer than a year on Venus. It takes 243 Earth days to rotate once on its axis.",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
        "The average person walks the equivalent of three times around the world in a lifetime.",
        "The Hawaiian alphabet has only 13 letters.",
        "A group of flamingos is called a 'flamboyance'.",
        "Octopuses have three hearts."
    ]
    return random.choice(facts)

def get_joke():
    """Return a random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Parallel lines have so much in common. It's a shame they'll never meet.",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "I used to play piano by ear, but now I use my hands.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them."
    ]
    return random.choice(jokes)

def get_system_info():
    """Get basic system information"""
    system_info = f"System: {platform.system()} {platform.version()}\n"
    system_info += f"Machine: {platform.machine()}\n"
    system_info += f"Processor: {platform.processor()}\n"
    return system_info

def get_battery_status():
    """Get battery status information"""
    try:
        # Use system command on macOS to get battery info
        result = subprocess.run(['pmset', '-g', 'batt'], capture_output=True, text=True)
        output = result.stdout
        
        if "No" in output and "batteries" in output:
            return "No battery found. Your Mac might be a desktop or the battery information is unavailable."
        
        # Parse the battery information
        battery_info = {}
        if "InternalBattery" in output:
            # Extract percentage
            percent_match = re.search(r'(\d+)%', output)
            if percent_match:
                battery_info['percent'] = percent_match.group(1)
            
            # Extract charging status
            if 'charging' in output.lower():
                battery_info['status'] = 'Charging'
            elif 'discharging' in output.lower():
                battery_info['status'] = 'Discharging'
            else:
                battery_info['status'] = 'Connected to power'
            
            # Extract time remaining if available
            time_match = re.search(r'(\d+:\d+) remaining', output)
            if time_match:
                battery_info['time_remaining'] = time_match.group(1)
            
            response = f"Battery at {battery_info.get('percent', 'unknown')}%. "
            response += f"Status: {battery_info.get('status', 'Unknown')}. "
            
            if 'time_remaining' in battery_info:
                response += f"Time remaining: {battery_info['time_remaining']}."
                
            return response
        else:
            return "Battery information is not available."
    except Exception as e:
        print(f"Error getting battery status: {e}")
        return "I couldn't retrieve the battery information at the moment."

def get_network_info():
    """Get network connectivity information"""
    try:
        # Check if we can connect to the internet
        socket.create_connection(("www.google.com", 80))
        
        # Get hostname and IP address
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        # Get Wi-Fi information on macOS
        result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], 
                                capture_output=True, text=True)
        airport_output = result.stdout
        
        network_info = f"Internet: Connected\n"
        network_info += f"Hostname: {hostname}\n"
        network_info += f"IP address: {ip_address}\n"
        
        # Extract Wi-Fi network name if available
        ssid_match = re.search(r' SSID: (.+)', airport_output)
        if ssid_match:
            network_info += f"Wi-Fi network: {ssid_match.group(1)}\n"
        
        return network_info
    except Exception as e:
        print(f"Error getting network info: {e}")
        return "Internet: Not connected or unable to retrieve network information."

def get_location_info():
    """Get approximate location based on IP address"""
    try:
        # Use IP-based geolocation (no GPS access needed)
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')
        loc = data.get('loc', '').split(',')
        timezone = data.get('timezone', 'Unknown')
        
        location_info = f"You appear to be in {city}, {region}, {country}.\n"
        
        # Set timezone based on location info
        os.environ['TZ'] = timezone
        
        # Also update our default weather city
        global default_location
        default_location = city
        
        if len(loc) == 2:
            location_info += f"Coordinates: {loc[0]}, {loc[1]}\n"
        
        location_info += f"Timezone: {timezone}"
        
        return location_info
    except Exception as e:
        print(f"Error getting location: {e}")
        return "I couldn't determine your location."

def get_disk_space():
    """Get disk space information"""
    try:
        # Get disk usage for the main disk
        total, used, free = shutil.disk_usage("/")
        
        # Convert to GB for readability
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)
        
        disk_info = f"Total disk space: {total_gb:.1f} GB\n"
        disk_info += f"Used space: {used_gb:.1f} GB\n"
        disk_info += f"Free space: {free_gb:.1f} GB\n"
        disk_info += f"Disk usage: {(used/total)*100:.1f}%"
        
        return disk_info
    except Exception as e:
        print(f"Error getting disk space: {e}")
        return "I couldn't retrieve disk space information."

def get_help():
    """Return help information about available commands"""
    help_text = "Here are some things you can ask me:\n"
    help_text += "- What's the time?\n"
    help_text += "- What's the date today?\n"
    help_text += "- What's the weather?\n"
    help_text += "- Where am I? / What's my location?\n"
    help_text += "- What's my battery status?\n"
    help_text += "- What's my IP address? / Network info?\n"
    help_text += "- How much disk space do I have?\n"
    help_text += "- Tell me a joke or fact\n"
    help_text += "- Play [song name] on YouTube\n"
    help_text += "- Search for [your query]\n"
    help_text += "- Open [website.com]\n"
    help_text += "- What should I do today?\n"
    
    return help_text

def listen():
	""" listen to what user says using Mac's default microphone with minimal output"""
	# This flag helps us control when to print the listening message
	
	try:
		# Create a fresh microphone source each time to prevent resource issues
		with sr.Microphone() as source:
			# Only print the message once if it hasn't been displayed yet
			if not hasattr(listen, 'message_displayed') or not listen.message_displayed:
				print("Listening for wake word '" + robot_name + "'...")
				listen.message_displayed = True
			
			# Adjust for ambient noise but with shorter duration to be more responsive
			listener.adjust_for_ambient_noise(source, duration=0.3)
			
			# Status indicator
			if port:
				port.write(b'l')  # Start with LEDs off
			
			# Listen for command with a timeout to prevent hanging
			try:
				voice = listener.listen(source, timeout=10, phrase_time_limit=5)
			except sr.WaitTimeoutError:
				# Just return silently and try again
				return
			
			try:
				# Use Google's speech recognition with US English specifically
				command = listener.recognize_google(voice, language="en-US").lower()
				
				# Look for wake word anywhere in the command
				if robot_name in command:
					# Print what was heard only when wake word is detected
					print(f"\nHeard: {command}")
					print(f"[Wake word '{robot_name}' detected!]")
					
					# Reset message flag to show listening again after processing
					listen.message_displayed = False
					
					if port:
						port.write(b'p')  # Show happy expression when activated
					
					# If wake word is not at the beginning, rearrange command
					if command.split(' ')[0] != robot_name:
						words = command.split()
						idx = words.index(robot_name)
						command = robot_name + " " + " ".join(words[:idx] + words[idx+1:])
					
					process(command)
					time.sleep(0.5)  # Brief pause after processing
				else:
					# No output if wake word not found
					if port:
						port.write(b'l')
			except sr.UnknownValueError:
				# No output for unrecognized audio
				if port:
					port.write(b'l')
			except sr.RequestError as e:
				# Only show critical errors
				print(f"\nNetwork Error: Could not request results; {e}")
				listen.message_displayed = False
				talk("I'm having trouble connecting to the speech recognition service")
				if port:
					port.write(b'l')
	except Exception as e:
		# Only show actual errors, not routine timeouts
		if not ("timed out" in str(e).lower() or "listening for" in str(e).lower()):
			print(f"\nError in listen function: {e}")
			listen.message_displayed = False
		
		if port:
			port.write(b'l')
		
		time.sleep(0.1)  # Brief pause to prevent CPU hogging

def process(words):
	""" process what user says and take actions """
	print(f"\n▶️  Processing command: {words}")
	print("-" * 40)
	
	# Log the command for debugging
	try:
		with open("command_log.txt", "a") as log:
			log.write(f"{datetime.now()}: {words}\n")
	except:
		pass
	
	# break words into list, ignoring wake word
	word_list = words.split(' ')[1:]
	
	# If just the wake word was said
	if len(word_list) == 0 or (len(word_list)==1 and word_list[0] == robot_name):
		talk("How can I help you today?")
		if port:
			port.write(b'h')  # Thinking expression
		return
		
	# Common daily questions processing
	full_text = ' '.join(word_list).lower()
	
	# Check for time-related queries
	if any(phrase in full_text for phrase in ["what time", "what's the time", "current time", "time now"]):
		talk(get_time_info())
		if port:
			port.write(b'p')  # Happy expression
		return
		
	# Check for date-related queries
	elif any(phrase in full_text for phrase in ["what date", "what day", "today's date", "what is today", "when is today"]):
		talk(f"Today is {get_date_info()}")
		if port:
			port.write(b'p')  # Happy expression
		return
	
	# Check for location-related queries
	elif any(phrase in full_text for phrase in ["where am i", "what's my location", "my current location"]):
		talk("Getting your location information")
		if port:
			port.write(b'h')  # Thinking expression
		
		location_info = get_location_info()
		talk(location_info)
		if port:
			port.write(b'p')  # Happy expression
		return
		
	# Check for battery status queries
	elif any(phrase in full_text for phrase in ["battery status", "how's my battery", "battery level", "power status"]):
		talk("Checking your battery status")
		if port:
			port.write(b'h')  # Thinking expression
		
		battery_info = get_battery_status()
		talk(battery_info)
		if port:
			port.write(b'p')  # Happy expression
		return
		
	# Check for network information queries
	elif any(phrase in full_text for phrase in ["network info", "what's my ip", "wifi status", "internet connection"]):
		talk("Checking your network information")
		if port:
			port.write(b'h')  # Thinking expression
		
		network_info = get_network_info()
		talk(network_info)
		if port:
			port.write(b'p')  # Happy expression
		return
		
	# Check for system information queries
	elif any(phrase in full_text for phrase in ["system info", "about my computer", "computer details", "system details"]):
		talk("Here's your system information")
		if port:
			port.write(b'h')  # Thinking expression
		
		system_info = get_system_info()
		talk(system_info)
		if port:
			port.write(b'p')  # Happy expression
		return
		
	# Check for disk space queries
	elif any(phrase in full_text for phrase in ["disk space", "storage info", "free space", "disk usage"]):
		talk("Checking your disk space")
		if port:
			port.write(b'h')  # Thinking expression
		
		disk_info = get_disk_space()
		talk(disk_info)
		if port:
			port.write(b'p')  # Happy expression
		return
		
	# Check for weather-related queries
	elif any(phrase in full_text for phrase in ["what's the weather", "weather today", "weather forecast", "how's the weather"]):
		talk("Checking the weather for you")
		if port:
			port.write(b'h')  # Thinking expression
		
		# Try to extract city name
		city_match = re.search(r"in ([a-zA-Z\s]+)$", full_text)
		if city_match:
			city = city_match.group(1).strip()
			weather_info = get_weather_info(city)
		else:
			# Use location from get_location_info if available
			try:
				location_info = get_location_info()
				if 'default_location' in globals() and default_location != "San Francisco":
					weather_info = get_weather_info(default_location)
				else:
					weather_info = get_weather_info()
			except:
				weather_info = get_weather_info()
		
		talk(weather_info)
		if port:
			port.write(b'p')  # Happy expression
		return
		
	# Check for joke requests
	elif any(phrase in full_text for phrase in ["tell joke", "tell me a joke", "know any jokes", "say something funny"]):
		if port:
			port.write(b'p')  # Happy expression
		talk(get_joke())
		return
		
	# Check for fact requests
	elif any(phrase in full_text for phrase in ["tell fact", "tell me a fact", "interesting fact", "random fact"]):
		if port:
			port.write(b'h')  # Thinking expression
		talk(get_fact())
		return
		
	# Check for help requests
	elif any(phrase in full_text for phrase in ["help me", "what can you do", "your commands", "how to use"]):
		if port:
			port.write(b'h')  # Thinking expression
		talk(get_help())
		return
	
	# Check for general well-being questions
	elif any(phrase in full_text for phrase in ["how are you", "how you doing", "how do you feel"]):
		responses = ["I'm doing well, thank you for asking!", 
		             "I'm functioning optimally today!", 
		             "All systems operational and ready to assist you!"]
		talk(random.choice(responses))
		if port:
			port.write(b'p')  # Happy expression
		return
	
	# "What to do today" type questions
	elif any(phrase in full_text for phrase in ["what to do", "what should i do", "i'm bored", "suggest activity"]):
		activities = [
			"How about reading a book?",
			"You could go for a walk and enjoy the fresh air.",
			"Maybe catch up on a TV series you've been meaning to watch.",
			"How about learning something new today?",
			"You could call a friend or family member you haven't spoken to in a while.",
			"Perhaps some exercise would be good for you today."
		]
		talk(random.choice(activities))
		if port:
			port.write(b'p')  # Happy expression
		return
		
	# Identity questions
	elif any(phrase in full_text for phrase in ["who are you", "what are you", "tell me about yourself"]):
		talk("I am Jarvis, your personal AI assistant. I can help you with daily tasks, answer questions, and control connected devices.")
		if port:
			port.write(b'p')  # Happy expression
		return

	if word_list[0] == 'play':
		"""if command for playing things, play from youtube"""
		talk("Okay boss, playing")
		extension = ' '.join(word_list[1:])                    # search without the command word
		if port:
			port.write(b'u')
		pywhatkit.playonyt(extension)   
		if port:
			port.write(b'l')          
		return

	elif word_list[0] == 'search' or word_list[0] == 'look' or word_list[0] == 'find':
		"""if command for google search"""
		if port:
			port.write(b'u')
		talk("Okay boss, searching")
		if port:
			port.write(b'h')  # Thinking expression
		extension = ' '.join(word_list[1:])
		pywhatkit.search(extension)
		if port:
			port.write(b'l')
		return

	if (word_list[0] == 'get') and (word_list[1] == 'info'):
		"""if command for getting info"""
		if port:
			port.write(b'u')
		talk("Okay, I am right on it")
		if port:
			port.write(b'u')
		extension = ' '.join(word_list[2:])                    # search without the command words
		inf = pywhatkit.info(extension)
		talk(inf)                                              # read from result             
		return

	elif word_list[0] == 'open':
		"""if command for opening URLs"""
		if port:
			port.write(b'l')
		talk("Opening, sir")
		url = f"http://{''.join(word_list[1:])}"   # make the URL
		webbrowser.open(url)
		return
	elif word_list[0] == 'angry' or word_list[0] == 'uppercut':
		if port:
			port.write(b'U')

	elif word_list[0] == 'sad' or word_list[0] == 'smash':
		if port:
			port.write(b's')

	elif word_list[0] == 'happy' or word_list[0] == 'punch':
		if port:
			port.write(b'p')
			
	elif word_list[0] == 'surprise' or word_list[0] == 'surprised':
		if port:
			port.write(b'a')

	# Handle generic questions - check if it's likely a question
	question_starters = ["what", "who", "when", "where", "why", "how", "is", "can", "could", "would", "will", "should"]
	
	if len(word_list) >= 2 and word_list[0].lower() in question_starters:
		if port:
			port.write(b'h')  # Thinking expression
		talk("Let me look that up for you")
		query = ' '.join(word_list)
		pywhatkit.search(query)
		return
	
	# now check for matches in specific words
	for word in word_list:
		if word in hi_words:
			""" if user says hi/hello greet him accordingly"""
			if port:
				port.write(b'h')               # send command for thinking expression
			talk(random.choice(hi_words))
			return

		elif word in bye_words:
			""" if user says bye etc"""
			if port:
				port.write(b's')               # send command for sad expression
			talk(random.choice(bye_words))
			return
			
		elif word in r_u_there:
			""" if user asks if assistant is there """
			if port:
				port.write(b'p')               # send command for happy expression
			talk("Yes, I'm here and ready to help!")
			return
	
	# Fallback for unrecognized commands
	talk("I'm not sure how to help with that. Would you like me to search the web for you?")
	if port:
		port.write(b'h')  # Thinking expression


def talk(sentence):
	""" talk / respond to the user through Mac's speakers with a female Siri-like voice """
	print(f"🤖 {sentence}")  # Print the response
	
	# After responding, reset the listening message flag
	listen.message_displayed = False
	
	# Try several voice output methods in order of reliability
	voice_output_success = False
	
	# Method 1: Use the globally initialized engine if available
	try:
		global voice_engine
		if voice_engine:
			print("Using pre-initialized voice engine...")
			
			# Speak with proper error handling
			voice_engine.say(sentence)
			
			# Run in try-except to catch any hanging issues
			try:
				voice_engine.runAndWait()
				voice_output_success = True
				print("Pre-initialized voice engine output completed")
			except RuntimeError as re:
				print(f"Error with pre-initialized engine: {re}")
				# Don't set success flag so we try other methods
	except Exception as e:
		print(f"Pre-initialized voice engine failed: {e}")
	
	# Method 2: Create a new pyttsx3 engine instance if needed
	if not voice_output_success:
		try:
			print("Attempting voice output with new pyttsx3 instance...")
			# Initialize the engine outside of any loop to avoid resource issues
			speech_engine = pyttsx3.init()
			
			# Get all available voices
			voices = speech_engine.getProperty('voices')
			karen_voice = None
			
			# Find Karen voice specifically
			for voice in voices:
				if 'karen' in voice.id.lower():
					karen_voice = voice.id
					print(f"Found Karen voice: {voice.id}")
					break
			
			# If Karen voice not found, find any female voice
			if not karen_voice:
				for voice in voices:
					voice_id = voice.id.lower()
					if any(name in voice_id for name in ["samantha", "siri", "female", "moira"]):
						karen_voice = voice.id
						print(f"Using alternative female voice: {voice.id}")
						break
			
			# Set the voice if found
			if karen_voice:
				speech_engine.setProperty('voice', karen_voice)
			
			# Set properties with good defaults for clear speech
			speech_engine.setProperty('rate', 165)      # Speed (slightly slower)
			speech_engine.setProperty('volume', 1.0)    # Volume
			
			# Speak with proper error handling
			speech_engine.say(sentence)
			
			# Run in try-except to catch any hanging issues
			try:
				speech_engine.runAndWait()
			except RuntimeError:
				print("Caught runtime error in runAndWait()")
				# Continue to cleanup
			
			# Cleanup - important to prevent resource issues
			try:
				speech_engine.stop()
			except:
				pass
			
			# Remove reference to the engine
			del speech_engine
			
			print("New pyttsx3 instance voice output completed")
			voice_output_success = True
		except Exception as e:
			print(f"New pyttsx3 instance voice output failed: {e}")
	
	# Method 3: If pyttsx3 failed, try subprocess for more direct control
	if not voice_output_success:
		try:
			print("Trying subprocess with say command...")
			import subprocess
			
			# Use a female voice explicitly and increase volume
			safe_sentence = sentence.replace('"', '\\"').replace("'", "\\'")
			subprocess.run(["say", "-v", "Karen", safe_sentence], check=True, timeout=10)
			
			print("Subprocess say command successful")
			voice_output_success = True
		except Exception as e:
			print(f"Subprocess say command failed: {e}")
	
	# Method 4: Last resort - direct OS command with specific voice and volume
	if not voice_output_success:
		try:
			print("Using direct OS system call...")
			safe_sentence = sentence.replace('"', '\\"').replace("'", "\\'")
			os.system(f"say -v Karen '{safe_sentence}'")
			print("OS system say command completed")
		except Exception as e:
			print(f"All voice output methods failed: {e}")
	
	# Add a separator line after response for cleaner output
	print("-" * 40)

# Initialize the text-to-speech engine
def initialize_tts_engine():
    """Initialize and configure the TTS engine for better performance"""
    global voice_engine
    try:
        print("🔊 Initializing text-to-speech engine...")
        voice_engine = pyttsx3.init()
        
        # Get all available voices
        voices = voice_engine.getProperty('voices')
        
        # Find and select Karen voice or other female voice
        karen_found = False
        for voice in voices:
            if 'karen' in voice.id.lower():
                voice_engine.setProperty('voice', voice.id)
                print(f"Using Karen voice: {voice.id}")
                karen_found = True
                break
        
        # If Karen voice not found, use another female voice
        if not karen_found:
            for voice in voices:
                if any(name in voice.id.lower() for name in ["samantha", "siri", "female", "moira"]):
                    voice_engine.setProperty('voice', voice.id)
                    print(f"Using alternative female voice: {voice.id}")
                    break
        
        # Set voice properties for clarity
        voice_engine.setProperty('rate', 165)  # Speed (slightly slower)
        voice_engine.setProperty('volume', 1.0)  # Full volume
        
        # Print all available voices for debugging
        print("\nAvailable voices:")
        for i, voice in enumerate(voices):
            print(f"{i+1}. {voice.id}")
        
        return voice_engine
    except Exception as e:
        print(f"Error initializing TTS engine: {e}")
        return None

# Function to test voice output
def test_voice():
    """Test if the voice output is working properly"""
    print("\n🔊 Testing voice output...")
    test_phrases = [
        "Hello, I am Jarvis, your personal assistant.",
        "I'm using a female voice similar to Siri.",
        "Voice test complete. Starting normal operation."
    ]
    
    for phrase in test_phrases:
        talk(phrase)
        time.sleep(0.5)
    
    return True

# Startup announcement
if __name__ == "__main__":
	print("\n" + "=" * 60)
	print(f"{' ' * 20}JARVIS AI Assistant")
	print("=" * 60)
	
	# Initialize a flag for displaying listening message
	listen.message_displayed = False
	
	# Clear terminal output for cleaner interface
	os.system('cls' if os.name == 'nt' else 'clear')
	
	print("\n🤖 Starting Jarvis AI Assistant...\n")
	
	# Initialize global voice engine
	voice_engine = initialize_tts_engine()
	
	# Announce system startup
	if port:
		port.write(b'a')  # Surprise expression on startup
		time.sleep(1)
	
	# Test the voice first
	test_voice()
	
	print("\n🎤 Say commands starting with 'Jarvis'")
	print("   For example: 'Jarvis, what time is it?'")
	print("   Press Ctrl+C to exit\n")
	
	# Reset function to reinitialize key components periodically
	def reset_components():
		"""Reset speech recognition and other components to prevent hanging"""
		global listener
		print("\n[System: Performing periodic reset to maintain responsiveness]")
		
		# Reinitialize the speech recognizer
		listener = sr.Recognizer()
		listener.energy_threshold = 4000
		listener.dynamic_energy_threshold = True
		listener.pause_threshold = 0.8
		
		# Reset the message display flag
		listen.message_displayed = False
		
		# Clear any resource-intensive processes
		try:
			import gc
			gc.collect()
		except:
			pass
		
		return time.time()
	
	# Track when we last reset components
	last_reset_time = time.time()
	
	# Main loop
	try:
		while True:
			# Periodically reset components to prevent hanging (every 5 minutes)
			if time.time() - last_reset_time > 300:  # 5 minutes in seconds
				last_reset_time = reset_components()
			
			listen()  # Listen for commands without cluttering the console
			
			# Short sleep to prevent CPU hogging
			time.sleep(0.1)
	except KeyboardInterrupt:
		print("\n\n" + "=" * 60)
		print("Shutting down Jarvis...")
		print("=" * 60)
		talk("Shutting down. Goodbye.")
		
		# Cleanup voice engine resources
		if 'voice_engine' in globals() and voice_engine:
			try:
				print("Cleaning up voice engine...")
				voice_engine.stop()
				del voice_engine
			except:
				pass
			
		# Cleanup Arduino connection
		if port:
			port.write(b's')  # Sad expression when shutting down
			time.sleep(1)
			port.write(b'l')  # Turn off all lights
			# Close the port properly
			try:
				port.close()
				print("Arduino connection closed.")
			except:
				pass
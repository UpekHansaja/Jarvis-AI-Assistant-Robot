#!/usr/bin/env python3
"""
Test script for JAUNDICE robot hardware
Run this to test individual functions before using voice commands
"""

import serial
import time
import glob

def find_arduino_port():
    """Find the Arduino serial port on macOS"""
    ports = glob.glob('/dev/tty.usbserial*') + glob.glob('/dev/tty.usbmodem*') + \
            glob.glob('/dev/cu.usbserial*') + glob.glob('/dev/cu.usbmodem*')
    
    if not ports:
        print("No Arduino found. Available ports:")
        all_ports = glob.glob('/dev/tty.*') + glob.glob('/dev/cu.*')
        usb_ports = [p for p in all_ports if 'usb' in p.lower()]
        for p in usb_ports:
            print(f"  {p}")
        return None
    
    return ports[0]

def test_robot():
    """Test all robot functions"""
    port_name = find_arduino_port()
    if not port_name:
        print("❌ No Arduino found!")
        return
    
    try:
        print(f"🔌 Connecting to Arduino on {port_name}")
        arduino = serial.Serial(port_name, 9600, timeout=2)
        time.sleep(2)  # Wait for Arduino to initialize
        
        print("🤖 Testing JAUNDICE Robot Functions...")
        
        # Test commands
        commands = [
            ('u', 'Activate LEDs'),
            ('h', 'Hand Wave'),
            ('p', 'Punch'),
            ('U', 'Uppercut'),
            ('s', 'Smash'),
            ('l', 'Deactivate LEDs')
        ]
        
        for cmd, description in commands:
            print(f"\n🎯 Testing: {description}")
            arduino.write(cmd.encode())
            time.sleep(2)
            
            # Read any response from Arduino
            while arduino.in_waiting:
                response = arduino.readline().decode().strip()
                if response:
                    print(f"   Arduino says: {response}")
        
        print("\n✅ Hardware test complete!")
        arduino.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_robot()

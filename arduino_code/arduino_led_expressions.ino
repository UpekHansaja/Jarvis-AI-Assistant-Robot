/*
 * JAUNDICE Robot Arduino Code (LED Expressions Version)
 * Controls LEDs for expressions based on serial commands from Python
 */

#include <Arduino.h>

// LED pins for expressions
const int happyLED = 3;     // Green LED (was rightArm)
const int sadLED = 5;       // Blue LED (was leftArm)
const int thinkingLED = 6;  // Yellow LED (was handWave)
const int angryLED = 9;     // Red LED (was smashServo)
const int statusLED = 11;   // Status LED (White)
const int builtInLED = 13;  // Built-in LED

// LED expression duration (milliseconds)
const int SHORT_PULSE = 300;
const int MEDIUM_PULSE = 500;
const int LONG_PULSE = 1000;

void setup() {
  Serial.begin(9600);
  
  // Setup LED pins
  pinMode(happyLED, OUTPUT);
  pinMode(sadLED, OUTPUT);
  pinMode(thinkingLED, OUTPUT);
  pinMode(angryLED, OUTPUT);
  pinMode(statusLED, OUTPUT);
  pinMode(builtInLED, OUTPUT);
  
  // Initialize all LEDs to OFF
  digitalWrite(happyLED, LOW);
  digitalWrite(sadLED, LOW);
  digitalWrite(thinkingLED, LOW);
  digitalWrite(angryLED, LOW);
  digitalWrite(statusLED, LOW);
  digitalWrite(builtInLED, LOW);
  
  Serial.println("JAUNDICE Robot Ready!");
  
  // Startup sequence - flash all LEDs
  startupSequence();
}

void startupSequence() {
  // Flash all LEDs once to indicate startup
  allLEDs(HIGH);
  delay(500);
  allLEDs(LOW);
}

void allLEDs(int state) {
  digitalWrite(happyLED, state);
  digitalWrite(sadLED, state);
  digitalWrite(thinkingLED, state);
  digitalWrite(angryLED, state);
  digitalWrite(statusLED, state);
  digitalWrite(builtInLED, state);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    switch(command) {
      case 'u': // Lights up / activate
        digitalWrite(statusLED, HIGH);
        digitalWrite(builtInLED, HIGH);
        Serial.println("Activated!");
        break;
        
      case 'l': // Lights off / deactivate  
        digitalWrite(statusLED, LOW);
        digitalWrite(builtInLED, LOW);
        Serial.println("Deactivated!");
        break;
        
      case 'U': // Uppercut expression (replaced with Angry pulse)
        Serial.println("Angry!");
        for(int i = 0; i < 3; i++) {
          digitalWrite(angryLED, HIGH);
          delay(SHORT_PULSE);
          digitalWrite(angryLED, LOW);
          delay(SHORT_PULSE);
        }
        break;
        
      case 'p': // Punch expression (replaced with Quick Happy)
        Serial.println("Happy!");
        digitalWrite(happyLED, HIGH);
        delay(MEDIUM_PULSE);
        digitalWrite(happyLED, LOW);
        break;
        
      case 's': // Smash expression (replaced with Sad)
        Serial.println("Sad!");
        digitalWrite(sadLED, HIGH);
        delay(LONG_PULSE);
        digitalWrite(sadLED, LOW);
        break;
        
      case 'h': // Hand wave (replaced with Thinking pattern)
        Serial.println("Thinking!");
        for(int i = 0; i < 3; i++) {
          digitalWrite(thinkingLED, HIGH);
          delay(MEDIUM_PULSE);
          digitalWrite(thinkingLED, LOW);
          delay(SHORT_PULSE);
        }
        break;

      case 'a': // All LEDs on (new expression - Surprise)
        Serial.println("Surprised!");
        allLEDs(HIGH);
        delay(MEDIUM_PULSE);
        allLEDs(LOW);
        break;
        
      default:
        Serial.println("Unknown command: " + String(command));
        break;
    }
  }
}

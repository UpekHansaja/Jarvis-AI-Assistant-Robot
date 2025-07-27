/*
 * JAUNDICE Robot Arduino Code
 * Controls servos and LEDs based on serial commands from Python
 */

#include <Servo.h>

// Create servo objects
Servo rightArm;    // Pin 3 - Punch
Servo leftArm;     // Pin 5 - Uppercut  
Servo handWave;    // Pin 6 - Wave
Servo smashServo;  // Pin 9 - Smash

// LED pins
const int statusLED = 11;
const int builtInLED = 13;

// Servo positions
const int REST_POS = 90;
const int PUNCH_POS = 45;
const int UPPERCUT_POS = 135;
const int WAVE_POS = 180;
const int SMASH_POS = 0;

void setup() {
  Serial.begin(9600);
  
  // Attach servos to pins
  rightArm.attach(3);
  leftArm.attach(5);
  handWave.attach(6);
  smashServo.attach(9);
  
  // Setup LED pins
  pinMode(statusLED, OUTPUT);
  pinMode(builtInLED, OUTPUT);
  
  // Initialize servos to rest position
  rightArm.write(REST_POS);
  leftArm.write(REST_POS);
  handWave.write(REST_POS);
  smashServo.write(REST_POS);
  
  Serial.println("JAUNDICE Robot Ready!");
  digitalWrite(builtInLED, HIGH);
  delay(1000);
  digitalWrite(builtInLED, LOW);
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
        
      case 'U': // Uppercut motion
        Serial.println("Uppercut!");
        leftArm.write(UPPERCUT_POS);
        delay(500);
        leftArm.write(REST_POS);
        break;
        
      case 'p': // Punch motion
        Serial.println("Punch!");
        rightArm.write(PUNCH_POS);
        delay(300);
        rightArm.write(REST_POS);
        break;
        
      case 's': // Smash motion
        Serial.println("Smash!");
        smashServo.write(SMASH_POS);
        delay(500);
        smashServo.write(REST_POS);
        break;
        
      case 'h': // Hand wave
        Serial.println("Waving!");
        for(int i = 0; i < 3; i++) {
          handWave.write(WAVE_POS);
          delay(300);
          handWave.write(REST_POS);
          delay(300);
        }
        break;
        
      default:
        Serial.println("Unknown command: " + String(command));
        break;
    }
  }
}

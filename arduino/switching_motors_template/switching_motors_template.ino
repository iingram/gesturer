#include <Servo.h>
// Servo definitions (line 2)
// Number of servos (line 3)
// Servo pin definitions (line 4)
// Type is "byte" so we get an unsigned 8-bit value
int data;
int currentServo = 0;

void setup() {
  // Attaching servos (line 10)
  Serial.begin(9600);
}

void loop() {
  // If Serial data is available
  if(Serial.available()) {
    // Read serial data and write back for error check
    data = Serial.read();      
    Serial.write(data);
    // Bounds check data for the motors
    if (data < 0) {
        data = 0;
    } else if (data > 180) {
      // Data exceeds 180 (24)
      // Else + switch for addressing scheme (25)
    } 
    // Switch on currentServo and write (27)
    // Increment the currentServo, and reset if over bounds (28)
  }
}

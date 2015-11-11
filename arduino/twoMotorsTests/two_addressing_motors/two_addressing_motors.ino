

#include <Servo.h>

Servo myServo0;
Servo myServo1;

int numServos = 2;

int servoPin0 = 13;
int servoPin1 = 7;
// Type is "byte" so we get an unsigned 8-bit value
int data;
int currentServo = 0;

void setup() {
  // TODO: Read in configurations/generate this file automatically??????
  myServo0.attach(servoPin0);
  myServo1.attach(servoPin1);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) {      // if data available
    // Read serial data and write back for error check
    data = Serial.read();      
    Serial.write(data);
    // Bounds check data for the motors
    if (data < 0) {
      data = 0;
    }
    // Bytes above 180 are addressing bytes
    if (data > 180) {
      currentServo = data - 181;
      currentServo = (currentServo < 0) ? 0 : currentServo;
    } else {
      switch (currentServo) {
        case 0:
          myServo0.write(data);
          break;
        case 1:
          myServo1.write(data);
          break;
      }
    }
  }
  
}

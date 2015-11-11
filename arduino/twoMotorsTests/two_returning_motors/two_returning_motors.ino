

#include <Servo.h>

Servo myServo0;
Servo myServo1;

int servoPin0 = 13;
int servoPin1 = 7;
// Type is "byte" so we get an unsigned 8-bit value
int data;
int currentServo = 0;

int servoPos0;
int servoPos1;

void setup() {
  // TODO: Read in configurations/generate this file automatically??????
  myServo0.attach(servoPin0);
  myServo1.attach(servoPin1);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) {      // if data available
    data = Serial.read();       // read data for first motor
//    if (data == 194) {
//      Serial.write(data);
//    } else {
    Serial.write(data);
    if (data > 180) {
      data = 180;
    } else if (data < 0) {
        data = 0;
    }
    if (currentServo == 0) {
      servoPos0 = data;
      myServo0.write(servoPos0);
    } else {
      servoPos1 = data;
      myServo1.write(servoPos1);
    }
    currentServo = !currentServo;
//    }
  }
  
}

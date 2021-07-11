

#include <Servo.h>

Servo myServo0;

int servoPin0 = 13;
// Type is "byte" so we get an unsigned 8-bit value
byte data;

int servoPos0;

void setup() {
  // put your setup code here, to run once:
  myServo0.attach(servoPin0);
  Serial.begin(9600);
  //Serial.println("Hello world!");
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()) {      // if data available
    data = Serial.read();       // read data for first motor
    if (data > 180) {
      data = 180;
    } else if (data < 0) {
        data = 0;
    }
    
    servoPos0 = (int) data;
    myServo0.write(servoPos0);
  }
  
//    if (servoPos > 90) {
//      myServo.write(180);
//    } else {
//      myServo.write(0);
//    }
//    if (data > 180) {
//      servoPos = data % 180;
//    } else if (data < 0) {
//      servoPos = data*-1;
//      servoPos = data % 180;
//    } else {
//      servoPos = data;
//    }
  
  
    //Serial.println(data);
    //delay(15); 
}

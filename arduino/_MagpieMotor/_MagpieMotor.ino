//** CONTROL GESTURE PROGRAM FOR MAGPIE ROBOT **
//**       Jonas Jørgensen                    **


#define LEDPin 13 // Onboard LED

//Pin locations for servo motors:

//Servo pin locations for the first magpie beak:
int mag1MotorAPin = 4;
int mag1MotorBPin = 6;
int mag1MotorCpin = 11;
//*Etc. for the other magpiebeaks

//Setup servos
#include <Servo.h>
Servo servo1A;
Servo servo1B;
Servo servo1C;

  //Time coordinate arrays for motors (miliseconds)
  int time1A[] = {0,1000, 2000, 3000, 4500, 5000};
  int time1B[] = {0,1000, 2000, 3000, 4500, 5000};
  int time1C[] = {0,500, 3500, 4000, 4500, 6000};
  //Angle coordinate array (in degrees)
  float angle1A[] = {0, 90, 0, 90, 0, 90}; //Magpie 1, motor A
  float angle1B[] = {0, 90, 0, 90, 0, 90}; //Magpie 1, motor B
  float angle1C[] = {0, 90, 0, 90, 0, 90}; //Magpie 1, motor C
  int numSamples = 6; //*Number of sample points*

//Variables used in loop:
unsigned long t = 0;
unsigned long offSetTime=0;
int a=0;
int b=0;
int c=0;
int p;

void setup() {
  //Setup servos
  servo1A.attach(mag1MotorAPin);
  servo1B.attach(mag1MotorBPin);
  servo1C.attach(mag1MotorCpin);
  //*Etc. for the rest of the servos.
 
  pinMode(LEDPin, OUTPUT); // Use LED indicator
  Serial.begin(9600);
  }

   
void loop() {

  t = millis(); //Set t to the number of miliseconds that has progressed since the program started
  t = t - offSetTime;
//  Serial.print(t);
//  Serial.print('\n');
//  Serial.print(offSetTime);
//  Serial.print('\n');
//  Serial.print('\n');


  if (t > time1A[a]){
    a++;  
    servo1A.write(angle1A[a]);

    Serial.print("[a]");
    Serial.print(angle1A[a]);
    Serial.print('\n');
    }

  if (t > time1B[b]){
    b++;  
    servo1B.write(angle1B[b]);

    Serial.print("[b]");
    Serial.print(angle1B[b]);
    Serial.print('\n');
    }
  
  if (t > time1C[c]){
    c++;  
    servo1C.write(angle1C[c]);

    Serial.print("[c]");
    Serial.print(angle1C[c]);
    Serial.print('\n');
    }
  

  delay(20); //Delay for servo signals to not exceed 500 Hz


p = max(a,b);
p = max(p,c);

  if (p >= numSamples){
    a = 0; //To start over
    b = 0;
    t = 0;
    digitalWrite(LEDPin, HIGH); //Turn pin on and wait, to indicate end of dataset has been reached
    delay(5000);
    digitalWrite(LEDPin, LOW);
    offSetTime = millis(); //New offSetTime is set 
    Serial.print("***************");
    Serial.print('\n');

  }

  }

//** CONTROL GESTURE PROGRAM FOR MAGPIE ROBOT **
//**       Jonas Jørgensen                    **


#define LEDPin 13 // Onboard LED

//Pin locations for servo motors:

//Servo pin locations for the first magpie:
int mag1MotorAPin = 6; //Neck
int mag1MotorAOffset = 0; //Neck
int mag1MotorABasePitch = 0; //Neck

int mag1MotorBPin = 7; //Pitch
int mag1MotorBOffset = 0; //Pitch

int mag1MotorCpin = 8; //Yaw
int mag1MotorCOffset = 0; //Yaw
int mag1MotorCBasePitch = 0; //Yaw

//*Etc. for the other magpiebeaks

//Setup servos
#include <Servo.h>
Servo servo1A;
Servo servo1B;
Servo servo1C;

  //****Time coordinate arrays for motors (miliseconds)
  //Magpie 1, motor A - Neck
  int time1A[] = {0,41,83,125,167,209,251,292,334,376,418,460,502,543,585,627,669,711,753,794,836,878,920,962,1004,1045,1087,1129,1171,1213,1255,1296,1338,1380,1422,1464,1506,1547,1589,1631,1673,1715,1757,1798,1840,1882,1924,1966,2008,2049,2091,2133,2175,2217,2259,2300,2342,2384,2426,2468,2510,2551,2593,2635,2677,2719,2761,2802,2844,2886,2928,2970,3012,3053,3095,3137,3179,3221,3263,3304,3346,3388,3430,3472,3514,3555,3597,3639,3681,3723,3765,3806,3848,3890,3932,3974,4016,4057,4099,4141,4183,4225,4267,4308,4350,4392,4434,4476,4518,4559,4601,4643,4685,4727,4769,4810,4852,4894,5187}; //Neck
  
  //Magpie 1, motor B - Pitch
  int time1B[] = {0,41,83,125,167,209,251,292,334,376,418,460,502,543,585,627,669,711,753,794,836,878,920,962,1004,1045,1087,1129,1171,1213,1255,1296,1338,1380,1422,1464,1506,1547,1589,1631,1673,1715,1757,1798,1840,1882,1924,1966,2008,2049,2091,2133,2175,2217,2259,2300,2342,2384,2426,2468,2510,2551,2593,2635,2677,2719,2761,2802,2844,2886,2928,2970,3012,3053,3095,3137,3179,3221,3263,3304,3346,3388,3430,3472,3514,3555,3597,3639,3681,3723,3765,3806,3848,3890,3932,3974,4016,4057,4099,4141,4183,4225,4267,4308,4350,4392,4434,4476,4518,4559,4601,4643,4685,4727,4769,4810,4852,4894,4936,4978,5020,5187};

  int time1C[] = {0,500, 3500, 4000, 4500, 6000};

  //****Angle coordinate array (in degrees)
  //Magpie 1, motor A - Neck
  float angle1A[] = {89,89,89,89,89,89,89,89,89,88,88,87,87,86,85,83,82,80,78,75,73,71,68,66,64,62,60,59,58,58,58,60,67,79,87,89,90,90,92,94,97,100,103,105,107,109,111,112,113,114,115,115,116,116,116,116,116,114,106,96,91,90,90,89,89,89,88,87,87,86,85,84,82,81,79,78,76,74,72,70,69,67,65,63,62,60,59,59,62,71,83,88,89,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,89,89,89,89,89,89,89,89}; 
  
  //Magpie 1, motor B - Pitch
  float angle1B[] = {3,3,3,4,4,5,6,7,8,9,11,13,14,17,19,21,23,26,28,30,32,34,36,38,39,40,41,42,42,43,43,42,42,41,39,37,35,33,31,30,28,27,27,27,28,29,30,32,33,35,37,39,40,42,43,43,43,43,43,42,41,40,38,36,35,33,32,30,29,28,28,28,28,28,29,30,31,32,33,34,36,37,39,40,41,41,42,42,42,41,41,40,39,38,37,36,34,33,31,30,28,27,26,25,24,23,22,20,18,17,14,12,10,8,7,6,5,4,4,3,3,3}; 

  float angle1C[] = {0, 90, 0, 90, 0, 90}; //Magpie 1, motor C
  int numSamples = 120; //*Number of sample points*

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
    servo1A.write(angle1A[a]+mag1MotorBOffset+mag1MotorABasePitch);

//    Serial.print("[a]");
//    Serial.print(angle1A[a]);
//    Serial.print('\n');
    }

  if (t > time1B[b]){
    b++;  
    servo1B.write(angle1B[b]+mag1MotorBOffset);

 //   Serial.print("[b]");
 //   Serial.print(angle1B[b]);
 //   Serial.print('\n');
    }
  
  if (t > time1C[c]){
    c++;  
    servo1C.write(angle1C[c]+mag1MotorCOffset+mag1MotorCBasePitch);

//    Serial.print("[c]");
//    Serial.print(angle1C[c]);
//    Serial.print('\n');
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

//READS CHARACTERS FROM CSV FILE ONE BY ONE INTO A STRING. 
//SEPARATES TIME AND ANGLE COORDINATES IN SEPARATE ARRAYS (INT AND FLOAT RESPECTIVELY).


// Builds on code from: http://www.jeremyblum.com/2011/04/05/tutorial-11-for-arduino-sd-cards-and-datalogging/

#include <SD.h>

//Set by default for the SD Card Library
//MOSI = Pin 11
//MISO = Pin 12
//SCK = PIN 13
//SDCS = pin 10

//Set the CS Pin:
int CS_pin = 10; //SDCS pin

//float refresh_rate = 0.0;

void setup()
{
 
  //Arrays for storing magpie time and angle coordinates:
  int time1A[255];
  float angle1A[255];
  int count=0; 
  
  Serial.begin(9600);
  Serial.println("Initializing Card");
  //CS Pin needs to be set as an output pin
  pinMode(CS_pin, OUTPUT);
    
  if (!SD.begin(CS_pin))
  {
      Serial.println("Card Failure");
      return;
  }
  Serial.println("Card Ready");
  
  //Read the file
  File commandFile = SD.open("ttt.csv");
  String tempTime;
  String tempAngle; 
  if (commandFile)
  {
    Serial.println("Reading file");
    char temp = 0;

    //Discard the first line of the file ("time, value" = 11 characters)
    for (int i=0; i < 11; i++)
    {
        temp = (commandFile.read()); //Read next character
    }
    tempTime = "";
    tempAngle = "";
    
    while(commandFile.available())
    {
      //1. Get time coordinate
      while(temp!=',')
      {
        //float temp = (commandFile.read() - '0'); 
        temp = (commandFile.read()); 
        tempTime = tempTime + temp; //Saves the character in the string
      }
      //Save time coordinate in array:
      tempTime = tempTime.substring(0, tempTime.length() - 1); //Delete separating comma
      time1A[count] = tempTime.toInt();//Save as int
      temp='0';

     
      //2. Get angle coordinate
      while(temp!='\n')
      {
        temp = (commandFile.read());
        tempAngle = tempAngle + temp; 
       }
      //Save angle coordinate in array:
      tempAngle = tempAngle.substring(0, tempAngle.length() - 1); //Delete newline character from string
      char floatbuf[32]; // Buffer
      tempAngle.toCharArray(floatbuf, sizeof(floatbuf));
      angle1A[count] = atof(floatbuf);//Save string as float

      
      //Print acquired data to serial connection
      Serial.println("@@@@@@@@@@@@@@@@@@@@@"); 
      Serial.println(time1A[count]); 
      Serial.println(angle1A[count]); 
      Serial.println("@@@@@@@@@@@@@@@@@@@@@"); 

      count++; //Increase index of time and angle strings 

      //Clear all temporary buffers:
      temp='0';
      tempTime=(char)0;
      tempAngle=(char)0;
      
    }
  }
  else
  {
    Serial.println("Could not read file.");
    return;
  }
  
}



void loop()
{
  
  String dataString = "Hello";
  
  //Open a file to write to
  //Only one file can be open at a time
  File logFile = SD.open("LOG.txt", FILE_WRITE);
//  if (logFile)
//  {
//    logFile.println(dataString);
//    logFile.close();
//    Serial.println(dataString);
//  }
//  else
//  {
//    Serial.println("LOG.txt");
//    Serial.println("Couldn't open log file");
//  }
//  delay(refresh_rate);
// delay(5000);
}

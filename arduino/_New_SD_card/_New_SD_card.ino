//READS CHARACTERS FROM CSV FILE ONE BY ONE INTO A STRING. 
//NEEDS TO ALSO SEPARATE TIME AND ANGLE COORDINATES IN SEPARATE ARRAYS.


// Fra: http://www.jeremyblum.com/2011/04/05/tutorial-11-for-arduino-sd-cards-and-datalogging/

#include <SD.h>

//Set by default for the SD Card Library
//MOSI = Pin 11
//MISO = Pin 12
//SCK = PIN 13
//SDCS = pin 10

//We always need to set the CS Pin
int CS_pin = 10; //SDCS pin
//int pow_pin = 8;

float refresh_rate = 0.0;

void setup()
{
  Serial.begin(9600);
  Serial.println("Initializing Card");
  //CS Pin is an output
  pinMode(CS_pin, OUTPUT);
  
  //Card will Draw Power from Pin 8, so set it high
//  pinMode(pow_pin, OUTPUT);  
//  digitalWrite(pow_pin, HIGH);
  
  if (!SD.begin(CS_pin))
  {
      Serial.println("Card Failure");
      return;
  }
  Serial.println("Card Ready");
  
  //Read the Configuration information (COMMANDS.txt)
  File commandFile = SD.open("ttt.csv");
  String tempTime; //***********
  String tempAngle; //***********
  if (commandFile)
  {
    Serial.println("Reading Command File");
    char temp = 0;

    //Discard the first line of the file ("time, value" = 11 characters) ***
    for (int i=0; i < 11; i++)
    {
        temp = (commandFile.read()); //********
        tempTime = tempTime + temp; //makes the string readString ************
    }
    tempTime = ""; //************
    
    while(commandFile.available())
    {
      //Get time coordinate ***
//      while(temp!=',')
      {
        //float temp = (commandFile.read() - '0'); 
        temp = (commandFile.read()); //********
      
        tempTime = tempTime + temp; //makes the string readString ************
        //refresh_rate = temp*decade+refresh_rate;
        //decade = decade/10;
        Serial.println(tempTime); //******
        Serial.println("*********"); //******
        //Serial.println(tempString); //******
      }
      //Get angle coordinate ***
      while(temp!=',')
      {
        //float temp = (commandFile.read() - '0'); 
        temp = (commandFile.read()); //********
    
        tempTime = tempTime + temp; //makes the string readString ************
        //refresh_rate = temp*decade+refresh_rate;
        //decade = decade/10;
        Serial.println(tempTime); //******
        //Serial.println(tempString); //******
       }
    }
//    Serial.print("Refresh Rate = ");
//    Serial.print(refresh_rate);
//    Serial.println("ms");
  }
  else
  {
    Serial.println("Could not read command file.");
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
 delay(10000);
}

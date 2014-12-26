import processing.serial.*;
import cc.arduino.*;

final boolean ARDUINO_CONNECTED = true;
final int OFFSET = -60;

String fileName1 = "../ttt.csv";
int motorPin1 = 7;
String fileName2 = "../ttt2.csv";
int motorPin2 = 6;
int motorPin3 = 4;

int scaleFactor = 4;

boolean going, looping;
GesturePlayer gestPlayer1;
GesturePlayer gestPlayer2;

Arduino arduino;
float drawAngle1, drawAngle2, drawAngle3;

void setup() {
  frameRate(240);
  size(180*scaleFactor, 100*scaleFactor);
  background(102);

  if (ARDUINO_CONNECTED) {
    println(Arduino.list());
    arduino = new Arduino(this, "COM3", 57600);
    arduino.pinMode(motorPin1, Arduino.SERVO);
    arduino.pinMode(motorPin2, Arduino.SERVO);
    arduino.pinMode(motorPin3, Arduino.SERVO);
  }

  drawAngle1 = 90;
  drawAngle2 = 90;
  drawAngle3 = 90;  
  // Fil3 f = new File(fileName1);
  // if (f.exists()){
  gestPlayer1 = new GesturePlayer(fileName1);
  // }
  // else{
  //	println("\nWARNING: DATA FILE DID NOT EXIST. EXITING. \n");//
  //	exit();
  //    }

  //  File f2 = new File(fileName2);
  //  if (f2.exists()){
  gestPlayer2 = new GesturePlayer(fileName2);
  //   }
  //  else{
  // 	println("\nWARNING: DATA FILE DID NOT EXIST. EXITING. \n");//
  // 	exit();
  //  }

  looping = false;
  going = false;
}

void draw() {
    if (going) {
      drawAngle1 = gestPlayer1.getPosition() + mouseY + OFFSET;
      drawAngle2 = gestPlayer2.getPosition();
      going = !(gestPlayer1.update(millis()));
      gestPlayer2.update(millis());
    } 
    else if (looping) {
      drawAngle1 = gestPlayer1.getPosition() + mouseY + OFFSET;
      drawAngle2 = gestPlayer2.getPosition();
      gestPlayer1.resetTime();
      gestPlayer2.resetTime();
      if (ARDUINO_CONNECTED) {
        arduino.servoWrite(motorPin1, constrain(int(drawAngle1), 0, 180));
        arduino.servoWrite(motorPin2, constrain(int(drawAngle2), 0, 180));
      }
      delay(1000);
      going = true;
    } 
    else {
      drawAngle1 = gestPlayer1.getPosition() + mouseY + OFFSET;
    }  
  drawAngle3 = mouseX;

  if (ARDUINO_CONNECTED) {
    arduino.servoWrite(motorPin1, constrain(int(drawAngle1), 0, 180));
    arduino.servoWrite(motorPin2, constrain(int(drawAngle2), 0, 180));
    arduino.servoWrite(motorPin3, constrain(int(drawAngle3), 0, 180));
  }

  drawUI();
  println(mouseX, mouseY);
}

void drawUI() {
  pushMatrix();
  background(100);
  // draw graduations: major are thick, minor thin
  for (int i = 0; i < 180; i+=5) {
    stroke(0);
    if (i%(15) == 0)
      strokeWeight(1);
    else
      strokeWeight(.1);
    line(i*scaleFactor, 0, i*scaleFactor, height);
  }

  //draw a vertical line at mouse position
  stroke(255, 0, 0);
  strokeWeight(2);
  line(mouseX, 0, mouseX, height);

  //draw button control key
  textSize(12);
  text("Click and mouse to gesture", width - 175, height - 75); 
  text("Press 'p' to play back", width - 175, height - 60);
  text("Press 'r' to rewind", width - 175, height - 45); 
  text("Press 'o' to loop", width - 175, height - 30); 
  text("Press 'q' to quit", width - 175, height - 15); 

  dial(width/4, height/2, drawAngle1);
  dial(2*width/4, height/2, drawAngle2);
  dial(3*width/4, height/2, drawAngle3);

  popMatrix();
}

void dial(int x, int y, float dAng) {
  //draw dial readout
  pushMatrix();
  translate(x, y);
  rotate(radians(dAng + 180));
  noStroke();
  ellipse(0, 0, 15, 15);
  rect(0, -2, 35, 4);
  popMatrix();
}

void keyReleased() {
  if (key == 'p')
    going = true;
  if (key == 'o')
    looping = !looping;
  if (key == 'r') {
    drawAngle1 = gestPlayer1.getPosition();
    //	drawAngle2 = gestPlayer2.getPosition();
    gestPlayer1.resetTime();
    //gestPlayer2.resetTime();
  }
  if (key == 'q')
    exit();
}


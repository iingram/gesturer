import processing.serial.*;
import cc.arduino.*;

final boolean ARDUINO_CONNECTED = true;

//these three lines you might want to edit
String fileName1 = "../curves/ttt.csv";
int motorPin1 = 4;
String fileName2 = "../curves/ttt2.csv";
int motorPin2 = 7;

int scaleFactor = 4;

// the rest of the code you probably want to leave as is
boolean going, looping;
GesturePlayer gestPlayer1;
GesturePlayer gestPlayer2;

Arduino arduino;
float drawAngle1, drawAngle2;

void setup() {
    size(180*scaleFactor, 100*scaleFactor);
    background(102);
    
    if(ARDUINO_CONNECTED){
	println(Arduino.list());
	arduino = new Arduino(this, "/dev/ttyUSB0", 57600);
	arduino.pinMode(motorPin1, Arduino.SERVO);
	arduino.pinMode(motorPin2, Arduino.SERVO);
    }

    drawAngle1 = 90;
    drawAngle2 = 90;

    File f = new File(fileName1);
    if (f.exists()){
	gestPlayer1 = new GesturePlayer(fileName1);
    }
    else{
	println("\nWARNING: DATA FILE DID NOT EXIST. EXITING. \n");//
	exit();
    }

    File f2 = new File(fileName2);
    if (f2.exists()){
    	gestPlayer2 = new GesturePlayer(fileName2);
    }
    else{
    	println("\nWARNING: DATA FILE DID NOT EXIST. EXITING. \n");//
    	exit();
    }
    
    looping = false;
    going = false;
}

void draw() {
    if (mousePressed == false) {
	
	if(going){
	    drawAngle1 = gestPlayer1.getPosition();
	    drawAngle2 = gestPlayer2.getPosition();
	    going = !(gestPlayer1.update(millis()));
	    gestPlayer2.update(millis());
	}
	else if(looping){
	drawAngle1 = gestPlayer1.getPosition();
	drawAngle2 = gestPlayer2.getPosition();
	gestPlayer1.resetTime();
	gestPlayer2.resetTime();
	if(ARDUINO_CONNECTED){
	    arduino.servoWrite(motorPin1, constrain(int(drawAngle1), 0, 180));
	    arduino.servoWrite(motorPin2, constrain(int(drawAngle2), 0, 180));
	}
	delay(1000);
	going = true;
	}
    }
    //move the motor
    if(ARDUINO_CONNECTED){
	arduino.servoWrite(motorPin1, constrain(int(drawAngle1), 0, 180));
	arduino.servoWrite(motorPin2, constrain(int(drawAngle2), 0, 180));
    }
    
    drawUI();
}

void drawUI(){
    pushMatrix();
    background(100);
    // draw graduations: major are thick, minor thin
    for(int i = 0; i < 180; i+=5){
	stroke(0);
	if(i%(15) == 0)
	    strokeWeight(1);
	else
	    strokeWeight(.1);
	line(i*scaleFactor,0,i*scaleFactor,height);
    }
    
    //draw a vertical line at mouse position
    stroke(255,0,0);
    strokeWeight(2);
    line(mouseX,0,mouseX,height);
    
    //draw button control key
    textSize(12);
    text("Click and mouse to gesture", width - 175, height - 75); 
    text("Press 'p' to play back", width - 175, height - 60);
    text("Press 'r' to rewind", width - 175, height - 45); 
    text("Press 'o' to loop", width - 175, height - 30); 
    text("Press 'q' to quit", width - 175, height - 15); 
    
    dial(width/3, height/2, drawAngle1);
    dial(2*width/3, height/2, drawAngle2);

    popMatrix();
}

void dial(int x, int y, float dAng){
    //draw dial readout
    pushMatrix();
    translate(x, y);
    rotate(radians(dAng + 180));
    noStroke();
    ellipse(0,0,15,15);
    rect(0, -2, 35, 4);
    popMatrix();
}

void keyReleased(){
    if(key == 'p')
	going = true;
    if(key == 'o')
	looping = !looping;
    if(key == 'r'){
	drawAngle1 = gestPlayer1.getPosition();
	//	drawAngle2 = gestPlayer2.getPosition();
	gestPlayer1.resetTime();
	//gestPlayer2.resetTime();
    }
    if(key == 'q')
	exit();
}


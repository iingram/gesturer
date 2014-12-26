import processing.serial.*;
import cc.arduino.*;

final boolean ARDUINO_CONNECTED = true;
final int OFFSET = -60;

String fileNamePitch = "../ttt.csv";
String fileNameNeck = "../ttt2.csv";

int motorPinPitch = 7;
int motorPinNeck = 6;
int motorPinYaw = 4;

int scaleFactor = 4;

boolean going, looping;
GesturePlayer gestPlayerPitch;
GesturePlayer gestPlayerNeck;

Arduino arduino;
float drawAnglePitch, drawAngleNeck, drawAngleYaw;
int basePitch = 58;
int baseYaw = 93;


void setup() {
    frameRate(240);
    size(180*scaleFactor, 100*scaleFactor);
    background(102);

    if (ARDUINO_CONNECTED) {
	println(Arduino.list());
	arduino = new Arduino(this, "/dev/ttyUSB0", 57600);
	arduino.pinMode(motorPinPitch, Arduino.SERVO);
	arduino.pinMode(motorPinNeck, Arduino.SERVO);
	arduino.pinMode(motorPinYaw, Arduino.SERVO);
    }

    drawAnglePitch = basePitch;
    drawAngleNeck = 90;
    drawAngleYaw = 90;  
    // Fil3 f = new File(fileNamePitch);
    // if (f.exists()){
    gestPlayerPitch = new GesturePlayer(fileNamePitch);
    // }
    // else{
    //	println("\nWARNING: DATA FILE DID NOT EXIST. EXITING. \n");//
    //	exit();
    //    }

    //  File f2 = new File(fileNameNeck);
    //  if (f2.exists()){
    gestPlayerNeck = new GesturePlayer(fileNameNeck);
    //   }
    //  else{
    // 	println("\nWARNING: DATA FILE DID NOT EXIST. EXITING. \n");//
    // 	exit();
    //  }

    looping = false;
    going = false;
}

void draw() {

    drawAnglePitch = gestPlayerPitch.getPosition() + basePitch + OFFSET;
    drawAngleNeck = gestPlayerNeck.getPosition();

    if (going) {
	going = !(gestPlayerPitch.update(millis()));
	gestPlayerNeck.update(millis());
    } 
    else if (looping) {
	gestPlayerPitch.resetTime();
	gestPlayerNeck.resetTime();
	if (ARDUINO_CONNECTED) {
	    arduino.servoWrite(motorPinPitch, constrain(int(drawAnglePitch), 0, 180));
	    arduino.servoWrite(motorPinNeck, constrain(int(drawAngleNeck), 0, 180));
	}
	delay(1000);
	going = true;
    } 

    drawAngleYaw = baseYaw;

    if(mouseX != pmouseX || mouseY != pmouseY){
	baseYaw = mouseX;
	basePitch = mouseY;
    }

    if (ARDUINO_CONNECTED) {
	arduino.servoWrite(motorPinPitch, constrain(int(drawAnglePitch), 0, 180));
	arduino.servoWrite(motorPinNeck, constrain(int(drawAngleNeck), 0, 180));
	arduino.servoWrite(motorPinYaw, constrain(int(drawAngleYaw), 0, 180));
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

    dial(width/4, height/2, drawAnglePitch);
    dial(2*width/4, height/2, drawAngleNeck);
    dial(3*width/4, height/2, drawAngleYaw);

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
	drawAnglePitch = gestPlayerPitch.getPosition();
	drawAngleNeck = gestPlayerNeck.getPosition();
	gestPlayerPitch.resetTime();
	gestPlayerNeck.resetTime();
    }
    if (key == 'q')
	exit();
}


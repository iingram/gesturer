import processing.serial.*;
import cc.arduino.*;

//these three lines you might want to edit
String fileName = "data.csv";
int motorPin = 4;
int scaleFactor = 4;

// rest of code you probably want to leave the same
boolean going;
GesturePlayer gestPlayer;
GestureRecorder gestRecorder;
Arduino arduino;
float drawAngle;
int pMX;

void setup() {
    size(180*scaleFactor, 100*scaleFactor);
    background(102);
    
    println(Arduino.list());
    arduino = new Arduino(this, "/dev/ttyUSB0", 57600);
    arduino.pinMode(motorPin, Arduino.SERVO);

    drawAngle = 90;
    pMX = -1;
    
    gestRecorder = new GestureRecorder(fileName);
    File f = new File(fileName);
    if (f.exists()){
	println("\nNOTE: THERE APPEARS TO BE AN EXISTING DATA FILE. OPENING IT FOR PLAYBACK. \n");//
	gestPlayer = new GesturePlayer(fileName);
    }
    else{
	println("\nWARNING: DATA FILE DID NOT EXIST. CREATING ONE. \n");//
	gestRecorder.clear();
	gestRecorder.addPosition(0);
	gestPlayer = new GesturePlayer(fileName);
    }
}

void draw() {
    background(100);
    
    if (mousePressed == false) {
	if(going){
	    drawAngle = gestPlayer.getPosition();
	    going = !(gestPlayer.update(millis()));
	}
	pMX = -1; 
    }
    else{
	if(pMX != mouseX){
	    drawAngle = constrain(mouseX/scaleFactor,0,180);
	    gestRecorder.addPosition(drawAngle);
	}
	pMX = mouseX;
    }

    //move the motor
    arduino.servoWrite(motorPin, constrain(int(drawAngle), 0, 180));

    // draw UI
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

    //draw dial readout
    translate(width/2, height/2);
    rotate(radians(drawAngle + 180));
    noStroke();
    ellipse(0,0,15,15);
    rect(0, -2, 35, 4);
}
 
void keyReleased(){
    if(key == 'g')
	going = true;
    if(key == 'r'){
	drawAngle = gestPlayer.getPosition();
	gestPlayer.resetTime();
    }
    if(key == 'q')
	exit();
}

void mousePressed(){
    gestRecorder.clear();
}

void mouseReleased(){
    going = false;
    gestPlayer.init(fileName);
}


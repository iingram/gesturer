import processing.serial.*;
import cc.arduino.*;

//these three lines you might want to edit
String fileName = "data.csv";
int motorPin = 4;
int scaleFactor = 4;

// the rest of the code you probably want to leave as is
boolean going, looping;
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
    if (mousePressed == false) {
	if(going){
	    drawAngle = gestPlayer.getPosition();
	    going = !(gestPlayer.update(millis()));
	}
	else if(looping){
	    drawAngle = gestPlayer.getPosition();
	    gestPlayer.resetTime();
	    arduino.servoWrite(motorPin, constrain(int(drawAngle), 0, 180));
	    delay(1000);
	    going = true;
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
    
    //draw dial readout
    translate(width/2, height/2);
    rotate(radians(drawAngle + 180));
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


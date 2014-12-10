import processing.serial.*;
import cc.arduino.*;

boolean going;
GesturePlayer gestPlayer;
GestureRecorder gestRecorder;

Arduino arduino;
Motor   motor;

float drawAngle = 0;
int pMX = -1;

final int SFACTOR = 4;

void setup() {
    size(180*SFACTOR, 100*SFACTOR);
    background(102);
    
    println(Arduino.list());
    arduino = new Arduino(this, "/dev/ttyUSB0", 57600);
    motor = new Motor(arduino, 4);
    drawAngle = 90;
    String fileName = "data.csv";
    
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
	    drawAngle = constrain(mouseX/SFACTOR,0,180);
	    gestRecorder.addPosition(drawAngle);
	}
	pMX = mouseX;
    }

    //move the motor
    motor.move(arduino,int(drawAngle));

    // draw UI
    // draw graduations: major are thick, minor thin
    for(int i = 0; i < 180; i+=5){
	stroke(0);
	if(i%(15) == 0)
	    strokeWeight(1);
	else
	    strokeWeight(.1);
	line(i*SFACTOR,0,i*SFACTOR,height);
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
    if(key == 'q')
	exit();
}

void mousePressed(){
    gestRecorder.clear();
}

void mouseReleased(){
    going = false;
    gestPlayer.init("data.csv");
}


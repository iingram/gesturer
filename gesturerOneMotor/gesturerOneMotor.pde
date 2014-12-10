import processing.serial.*;
import cc.arduino.*;

boolean going;
GesturePlayer gestPlayer;
GestureRecorder gestRecorder;

Arduino arduino;
Motor   motor;

float drawAngle = 0;

void setup() {
    size(180, 50);
    background(102);
    
    println(Arduino.list());
    arduino = new Arduino(this, "/dev/ttyUSB0", 57600);
    motor = new Motor(arduino, 4);
    drawAngle = 90;
    
    gestPlayer = new GesturePlayer("data.csv");
    gestRecorder = new GestureRecorder("data.csv");
}

void draw() {
    background(100);
    
    if (mousePressed == false) {
	if(going){
	    going = !(gestPlayer.update(millis()));
	    drawAngle = gestPlayer.getPosition();
	}
    }
    else{
	if(pmouseX != mouseX){
	    drawAngle = constrain(mouseX,0,180);
	    gestRecorder.addPosition(drawAngle);
	}
    }
    for(int i = 0; i < 180; i+=5){
	stroke(0);
	if(i%(15) == 0)
	    strokeWeight(1);
	else
	    strokeWeight(.1);
	line(i,0,i,height);
    }
    stroke(255,0,0);
    strokeWeight(2);
    line(mouseX,0,mouseX,height);

    translate(width/2, height/2);
    rotate(radians(drawAngle + 180));
    noStroke();
    ellipse(0,0,15,15);
    rect(0, -2, 35, 4);
    
    motor.move(arduino,int(drawAngle)); //CHECK RANGE MAY NOT BE FULL    
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


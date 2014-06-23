class Motor {
    int pinNum;

    Motor(Arduino arduino) {
	pinNum = 9;
	//	arduino = new Arduino(thisAgain, "/dev/ttyUSB0", 57600);
	arduino.pinMode(pinNum, Arduino.SERVO);
	
    }
    
    Motor(Arduino arduino, int iPinNum) {
	pinNum = iPinNum;
	//	arduino = new Arduino(thisAgain, "/dev/ttyUSB0", 57600);
	arduino.pinMode(pinNum, Arduino.SERVO);
    }
    
    void move(Arduino arduino, int pos) {
	arduino.servoWrite(pinNum, constrain(pos, 0, 180));
    }
    
    void move(Arduino arduino, float pos) {
	arduino.servoWrite(pinNum, int(constrain(pos, 0, 180)));
    }
}


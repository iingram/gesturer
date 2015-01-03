import processing.serial.*;
import cc.arduino.*;
import de.looksgood.ani.*;

final boolean ARDUINO_CONNECTED = false;
final int OFFSET = -60;

String toEncode = "This is a test message.";
String encodedMessage;
int currentIndexInMessage = 0;
final char DOT = '.';
final char DASH = '-';
final char LETTER_BOUNDARY = '/';
final char SPACE = ' ';
final int DOT_BASEINDEX = 0;
final int DASH_BASEINDEX = 1;
final int LETTER_BOUNDARY_BASEINDEX = 2;
final int SPACE_BASEINDEX = 3;

String fileNamePitch = "/Users/reidmitchell/Code/gesturer/gesturerMagpie/data/curves/ttt.csv";
String fileNameNeck = "/Users/reidmitchell/Code/gesturer/gesturerMagpie/data/curves/ttt.csv";

int motorPinPitch = 7;
int motorPinNeck = 6;
int motorPinYaw = 4;

int scaleFactor = 4;

boolean going, looping, transitioning, gesturing, firstTime;
GesturePlayer gestPlayerPitch;
GesturePlayer gestPlayerNeck;

Arduino arduino;
float drawAnglePitch, drawAngleNeck, drawAngleYaw;
int basePitch;
int baseYaw;
int baseNeck;

//int[][] bases = new int[3][2];
int[][] bases = {
  {
    72, 72, 72 // DOT '.'
  }
  , {
    144, 144, 144 // DASH '-'
  }
  , {
    216, 216, 216 // LETTER BOUNDARY '/'
  }
  , {
    288, 288, 288 // SPACE ' '
  }
};
int baseIndex = -1;

void setup() {
  frameRate(240);
  size(180*scaleFactor, 100*scaleFactor);
  background(102);

  if (ARDUINO_CONNECTED) {
    println(Arduino.list());
    arduino = new Arduino(this, "/dev/ttyUSB1", 57600);
    arduino.pinMode(motorPinPitch, Arduino.SERVO);
    arduino.pinMode(motorPinNeck, Arduino.SERVO);
    arduino.pinMode(motorPinYaw, Arduino.SERVO);
  }
  
  encodedMessage = encodeMorse(toEncode);
  println(encodedMessage);
  
  baseNeck = bases[0][2];
  basePitch = bases[0][1];
  baseYaw = bases[0][0];

  drawAnglePitch = 90;
  drawAngleNeck = 90;
  drawAngleYaw = 90;  

  // Fil3 f = new File(fileNamePitch);
  // if (f.exists()){
  gestPlayerPitch = new GesturePlayer(fileNamePitch);
  // }
  // else{
  //  println("\nWARNING: DATA FILE DID NOT EXIST. EXITING. \n");//
  //  exit();
  //    }

  //  File f2 = new File(fileNameNeck);
  //  if (f2.exists()){
  gestPlayerNeck = new GesturePlayer(fileNameNeck);
  //   }
  //  else{
  //   println("\nWARNING: DATA FILE DID NOT EXIST. EXITING. \n");//
  //   exit();
  //  }

  looping = false;
  going = false;
  transitioning = false;
  firstTime = false;

  gestPlayerPitch.resetTime();
  gestPlayerNeck.resetTime();

  Ani.init(this);
}

void draw() {

  drawAnglePitch = gestPlayerPitch.getPosition() + basePitch + OFFSET;
  drawAngleNeck = gestPlayerNeck.getPosition();
  drawAngleYaw = baseYaw;

  if (going && transitioning && firstTime) {
    // cycle begins for a new character: find the next base and transition to that base
    // (loop back to beginning if there are no characters left in the encoded message && looping=true)
    if(currentIndexInMessage >= encodedMessage.length()) {
      currentIndexInMessage = 0;
    }
    baseIndex = getNextBaseIndex();
    Ani.to(this, 2.5, "baseNeck", bases[baseIndex][2], Ani.QUINT_IN_OUT);
    Ani.to(this, 2.5, "basePitch", bases[baseIndex][1], Ani.QUINT_IN_OUT);
    Ani.to(this, 2.5, "baseYaw", bases[baseIndex][0], Ani.QUINT_IN_OUT);
    firstTime = false;
  }
  else if (going && transitioning && !firstTime) {
    // wait for transition to complete before beginning the gesture
    if(baseNeck==bases[baseIndex][2] && basePitch==bases[baseIndex][1] && baseYaw==bases[baseIndex][0]) {
      transitioning = false;
    }
  }
  else if (going && !transitioning) {
    // perform the gesture
    going = !(gestPlayerPitch.update(millis()));
    gestPlayerNeck.update(millis());
  }
  else if (going && !transitioning && !firstTime) {
    println("lol"+millis()); 
  }
  else if (!going && !transitioning && !firstTime) {
    // gesture complete. restart the cycle: transition -> perform gesture -> finish gesture
    going = transitioning = firstTime = true;
    
    gestPlayerPitch.resetTime();
    gestPlayerNeck.resetTime();
  }

  if (mouseX != pmouseX || mouseY != pmouseY) {
    baseYaw = mouseX;
    basePitch = mouseY;
  }

  if (ARDUINO_CONNECTED) {
    arduino.servoWrite(motorPinPitch, constrain(int(drawAnglePitch), 0, 180));
    arduino.servoWrite(motorPinNeck, constrain(int(drawAngleNeck), 0, 180));
    arduino.servoWrite(motorPinYaw, constrain(int(drawAngleYaw), 0, 180));
  }

  drawUI();
  //println(mouseX, mouseY);
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

  String ms;
  ms = String.format("MouseX is %d" + " Mouse Y is %d, ", mouseX, mouseY);

  //draw button control key
  textSize(12);
  text(ms, width - 175, height - 125);
  text("Current base: "+baseIndex, width - 175, height - 110);
  text("Press 'i' for next base", width - 175, height - 95);
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
    transitioning = true;
    firstTime = true;
  if (key == 'o')
    looping = !looping;
  if (key == 'i') {
    baseIndex++;
    if (baseIndex > bases.length - 1)
      baseIndex = 0;
    Ani.to(this, 2.5, "baseNeck", bases[baseIndex][2], Ani.QUINT_IN_OUT);
    Ani.to(this, 2.5, "basePitch", bases[baseIndex][1], Ani.QUINT_IN_OUT);
    Ani.to(this, 2.5, "baseYaw", bases[baseIndex][0], Ani.QUINT_IN_OUT);
    // basePitch = bases[baseIndex][1];
    // baseYaw = bases[baseIndex][0];
  }
  if (key == 'r') {
    drawAnglePitch = gestPlayerPitch.getPosition();
    drawAngleNeck = gestPlayerNeck.getPosition();
    gestPlayerPitch.resetTime();
    gestPlayerNeck.resetTime();
  }
  if (key == 'q')
    exit();
}

int getNextBaseIndex() {
  println("currentIndexInMessage: "+currentIndexInMessage);
  char c = encodedMessage.charAt(currentIndexInMessage);
  switch(c) {
    case DOT: currentIndexInMessage++; return DOT_BASEINDEX;
    case DASH: currentIndexInMessage++; return DASH_BASEINDEX;
    case LETTER_BOUNDARY: currentIndexInMessage++; return LETTER_BOUNDARY_BASEINDEX;
    case SPACE: currentIndexInMessage++; return SPACE_BASEINDEX;
  }
  return -1;
}

String encodeMorse(String m) {
  m = m.toUpperCase();
  String out = ""; 
  for(int i=0; i<m.length(); i++) {
    char c = m.charAt(i);
    switch(c) {
      case 'A': out+= ".-"; break;
      case 'B': out+= "-..."; break;
      case 'C': out+= "-.-."; break;
      case 'D': out+= "-.."; break;
      case 'E': out+= "."; break;
      case 'F': out+= "..-."; break;
      case 'G': out+= "--."; break;
      case 'H': out+= "...."; break;
      case 'I': out+= ".."; break;
      case 'J': out+= ".---"; break;
      case 'K': out+= "-.-"; break;
      case 'L': out+= ".-.."; break;
      case 'M': out+= "--"; break;
      case 'N': out+= "-."; break;
      case 'O': out+= "---"; break;
      case 'P': out+= ".--."; break;
      case 'Q': out+= "--.-"; break;
      case 'R': out+= ".-."; break;
      case 'S': out+= "..."; break;
      case 'T': out+= "-"; break;
      case 'U': out+= "..-"; break;
      case 'V': out+= "...-"; break;
      case 'W': out+= ".--"; break;
      case 'X': out+= "-..-"; break;
      case 'Y': out+= "-.--"; break;
      case 'Z': out+= "--.."; break;
      case '0': out+= "-----"; break;
      case '1': out+= ".----"; break;
      case '2': out+= "..---"; break;
      case '3': out+= "...--"; break;
      case '4': out+= "....-"; break;
      case '5': out+= "....."; break;
      case '6': out+= "-...."; break;
      case '7': out+= "--..."; break;
      case '8': out+= "---.."; break;
      case '9': out+= "----."; break;
      case '.': out+= ".-.-.-"; break;
      case ',': out+= "--..--"; break;
      case ':': out+= "---..."; break;
      case '?': out+= "..--.."; break;
      case '\'': out+= ".----."; break;
      case '-': out+= "-....-"; break;
      case '/': out+= "-..-."; break;
      case '(': out+= "-.--."; break;
      case ')': out+= "-.--.-"; break;
      case '"': out+= ".-..-."; break;
      case '@': out+= ".--.-."; break;
      case '=': out+= "-...-"; break;
      case ' ': out+= SPACE; break;
    }
    out+=LETTER_BOUNDARY;
  }
  return out;
}


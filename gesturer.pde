/* gesturer.pde
Modified by Skyler Williams beginning 09/19/2015


?: Gestures either a gesture read in from TIME_CURVE_FILENAME or from fileName, 
and writes newly created gestures to fileName.

?: In the sketch itself, a user can either create a gesture while pressing the 
mouse and have it played back by all the motors when the mouse is not pressed,
or a user can input a gesture to be played when the mouse is not pressed. 
The motors always follow the mouse while it is pressed.

*/



// Import statements
import processing.serial.*;
import cc.arduino.*;


// Global variables
final String fileName = "data.csv";
final String usbPort = "/dev/ttyUSB0";
final String TIME_CURVE_FILENAME = "curves/timeCurve.csv";
final String dirPath = sketchPath("");
final String filePath = dirPath + "/" + fileName;

// ?: Whether we will read in a time curve
final boolean USE_OWN_CURVE = true;
final boolean ARDUINO_CONNECTED = false;

// ?: Number of motors in use for project
final int NUM_MOTORS = 3;

final int SFACTOR = 2;

// ?: Do we want a "looping" array here as well? This is the case in twoMotors
//    but with booleans
// ?: Array representing if the motors are running or not
boolean going[] = new boolean[NUM_MOTORS];
// ?: Array of GesturePlayers to play gestures on each motor
GesturePlayer[] gestPlayer = new GesturePlayer[NUM_MOTORS];
GestureRecorder gestRecorder, tempRecorder;

Arduino arduino;
Motor[] motor = new Motor[NUM_MOTORS];

float[] drawAngle = new float[NUM_MOTORS];
// ?: X position of the pointer/dial
int pMX = -1;


// Function declarations

/*
 *
 */
void setup() {
    // Set size to an initial value, as size() requires numbers not variables
    size(100,100);

    // Resize the sketch to be the desired dimensions
    int xSize = 180*SFACTOR;
    int ySize = 100*SFACTOR;
    surface.setSize(xSize, ySize);
    
    background(102);

    // Initialize the Arduino
    if (ARDUINO_CONNECTED) {
        println(Arduino.list());
        arduino = new Arduino(this, usbPort, 57600);
    }

    // Initialize motors
    // TODO: Read in the motors' pins from a file, error if mismatch on number
    //       of motors?
    for (int i = 0; i < motor.length; i++) {
        if (ARDUINO_CONNECTED) {
            motor[i] = new Motor(arduino, 10-NUM_MOTORS+i);
        }
        drawAngle[i] = 80/MOVE_GAIN_0;
    }

    gestRecorder = new GestureRecorder(fileName);

    // TODO: make this generalized to read in a data file for each motor
    // If using own curve, read in the file 
    if (USE_OWN_CURVE) {
        if (fileExists(filePath)) {
            println("\nNOTE: THERE APPEARS TO BE AN EXISTING DATA FILE. WILL USE IT. \n");
        } else {
            println("\nWARNING: DATA FILE DID NOT EXIST. CREATING ONE. \n");
            // Creating new data file
            gestRecorder.clear();
            gestRecorder.addPosition(0);
        }
    }

    // Initialize the gesturePlayer for each motor with the appropriate gesture file
    // NOTE: Currently, this assigns the same gesture to each motor
    // TODO: Make this an input/configuation file toggleable option, so we can have 
    // different gestures for different motors, read in these files in the section 
    // directly above. Use JSON for the config files so we can directly create 
    // objects.
    for (int i = 0; i < gestPlayer.length; i++) {
        // If using own curve, each GesturePlayer is initialized with the 
        // existing data file as its gesture
        if (USE_OWN_CURVE) {
            gestPlayer[i] = new GesturePlayer(fileName);
        } else {
            // If the data file exists, create a new GesturePlayer with file
            if (fileExists(dirPath + "/" + TIME_CURVE_FILENAME)) {
                gestPlayer[i] = new GesturePlayer(TIME_CURVE_FILENAME);
            }
            // Otherwise, create a new data file and a GesturePlayer init'ed
            // with the file
            else {
                tempRecorder = new GestureRecorder(TIME_CURVE_FILENAME);
                tempRecorder.clear();
                tempRecorder.addPosition(0);
                gestPlayer[i] = new GesturePlayer(TIME_CURVE_FILENAME);
            }
        }
        // Turn off each motor
        going[i] = false;
    }

    //init to start position
    drawAngle[0] = gestPlayer[0].getPosition();
    for (int i = 0; i < gestPlayer.length; i++) {
        gestPlayer[i].resetTime();
    }
}


/*
 *
 */
void draw() {
    thread("readPipe");
    background(100);
    
    // Update positions for a dial based on mouse position and pressed status
    if (mousePressed == false) {
        // ?: If the mouse is not pressed, for each motor that is going set the
        //    draw angle equal to their current Player position (aka. moving 
        //    the motors in their gestures when the mouse is not pressed)
        for (int i = 0; i < gestPlayer.length; i++) {
            if (going[i]) {
                going[i] = !(gestPlayer[i].update(millis()));
                drawAngle[i] = gestPlayer[i].getPosition();
            }
        }
        // Set to -1 so it cannot be equal to mouseX
        pMX = -1;
    } else { // If the mouse is pressed
        // ?: If the pressedMouseX is not equal to the mouseX
        if (pMX != mouseX) {
            // For each motor, set the draw angle based on the mouse
            for (int i = 0; i < gestPlayer.length; i++) {
                drawAngle[i] = constrain(mouseX/SFACTOR,0,180);
            }
            // Record the input gesture
            gestRecorder.addPosition(drawAngle[0]);
        }
        // Set the pressed value equal to mouseX so we don't repeat the
        // previous work unnecessarily when the mouse is held at a location
        pMX = mouseX;
    }

    // Draw a stripey background!
    for (int i = 0; i < 180; i+=5) {
        stroke(0);

        if (i%(15) == 0) {
            strokeWeight(1);
        } else {
            strokeWeight(.1);
        }

        line(i*SFACTOR,0,i*SFACTOR,height);
    }

    // Draw a verticle line indidcation mouse location
    stroke(255,0,0);
    strokeWeight(2);
    line(mouseX,0,mouseX,height);

    // Draw the dial rotated to the angle of the first motor
    translate(width/2, height/2);
    rotate(radians(drawAngle[0] + 180));
    noStroke();
    ellipse(0,0,15,15);
    rect(0, -2, 35, 4);

    // If an Arduino is connected, move motors to their drawAngles
    if (ARDUINO_CONNECTED) {
        for (int i = 0; i < motor.length; i++) {
            motor[i].move(arduino,int(drawAngle[i])); //CHECK RANGE MAY NOT BE FULL   
        }
    } 
}
 

/*
 *
 */
void keyReleased() {
    // Sets first motor going
    if (key == '1') {
        going[0] = true;
    }
    // Sets second motor going
    if (key == '2') {
        going[1] = true;
    }
    // Sets third motor going
    if (key == '3') {
        going[2] = true;
    }
    // Exists the program
    if (key == 'w') {
        exit();
    }
}


/*
 *
 */
void mousePressed() {
    gestRecorder.clear();
}


/*
 *
 */
void mouseReleased() {
    // Turn off each motor and init with fileName gesture
    for (int i = 0; i < gestPlayer.length; i++) {
        going[i] = false;
        gestPlayer[i].init(fileName);
    }
}


/*
 *
 */
void readPipe() {
    // Load the lines of sharingPlace.tmp into an array
    String[] s = loadStrings("sharingPlace.tmp");
    // Grab the first line of sharingPlace.tmp
    int level = int(s[0]);

    // If first line is a 1, set the first motor going
    if (level == 1) {
        going[0] = true;
    // If the first line is a 2, set the first 2 motors going
    } else if (level == 2) {
        going[0] = true;
        going[1] = true;
    }
}


/*
 *
 */
boolean fileExists(String path) {
    File file = new File(path);
    return file.exists();
} 

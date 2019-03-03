//#include <Servo.h>
#include <VarSpeedServo.h>

VarSpeedServo drop_motor;
VarSpeedServo flip_motor;


const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

#define CLOSER_PIN 9
static int DROP_OPEN = 90;
static int DROP_CLOSED = 140;
static int DROP_SPEED = 100;
int drop_pos = 0;
int drop_target_pos = DROP_CLOSED;
bool dropped = false;

#define FLIP_PIN 10
static int FLIP_NORMAL = 60;
static int FLIP_OPEN = 180;
static int FLIP_SPEED = 255;
int flip_pos = 0;
int flip_target_pos = FLIP_NORMAL;
bool flip = false;

bool runProgram = true;


void setup() {
  Serial.begin(9600);
  Serial.println("Arduino is ready");
   
  drop_motor.attach(CLOSER_PIN);  // attaches the servo on pin 9 to the servo object
  flip_motor.attach(FLIP_PIN);
  move_mail();
  move_flip();
  
  
}

void loop() {
  Serial.println("Program Started. Use 'd' to drop, 'o' to open, 'c' to close, 'f' to flip, 'q' to quit, 'r' to restart");
  while (runProgram) {
    handleSerial();
    drop_mail();
//    move_mail();
    move_flip();
    delay(15);
  }
  while (!runProgram) {
    Serial.println("Program Stopped. Use 'r' to restart");
    handleSerial();
    delay(2000);
  }
}

void handleSerial(){
  while (Serial.available() > 0){
    char incomingChar = Serial.read();
    switch (incomingChar){
      case 'o': //open
        Serial.println("Opening Drop");
        drop_target_pos = DROP_OPEN;
      break;
      
      case 'c': //close
        Serial.println("Closing Drop");
        drop_target_pos = DROP_CLOSED;
      break;

      case 'd':
        Serial.println("Dropping");
        dropped = false;
       break;

      case 'f': //flip
        Serial.println("Flipping");
        flip = true;
       break;

//       case 'u': //unflip
//        flip_target_pos = FLIP_NORMAL;
//       break;
      
      case 'q': //quit
        Serial.println("Shutting Down");
        drop_target_pos = DROP_CLOSED;
        runProgram = false;
        Serial.println("Shut Down. Ok To Turn Off");
      break;

      case 'r': //restart or start
        Serial.println("Starting Program");
        runProgram = true;
        Serial.println("Program Started");
      break;
    }
  }
}


void move_mail(){
  drop_motor.slowmove(drop_target_pos, DROP_SPEED);
}

void drop_mail(){
//  drop_motor.slowmove(DROP_OPEN, DROP_SPEED);

  if (!dropped && drop_motor.read() > DROP_OPEN){
    drop_motor.slowmove(DROP_OPEN, DROP_SPEED);
  }
  else if (!dropped && drop_motor.read() <= DROP_OPEN){
    delay(1000);
    dropped = true;
  }
  else{
    drop_motor.slowmove(DROP_CLOSED, DROP_SPEED);
  }
}

void move_flip(){
  if (flip && flip_motor.read() < FLIP_OPEN){
    flip_motor.slowmove(FLIP_OPEN, FLIP_SPEED);
//    Serial.println(flip_motor.read());
  }
  else{
    flip = false;
    flip_motor.write(FLIP_NORMAL);
  }
}


  

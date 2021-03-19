#include <Servo.h>

Servo elbow_servo;
Servo elbow_servo2;
Servo wrist_servo;
Servo level_servo;

//initiaties pins on arduino
const int button_pin = 2;
const int led_pin = 4;
const int x_pin = 0;
const int y_pin = 1;

int chicken = 0;
float elbow_angle = 90; //degrees
float elbow_angle_old = 90; //degrees
float wrist_angle = 90; //degrees
float wrist_angle_old = 90; //degrees
float level_angle = 90; //degrees
float level_angle_old = 90; //degrees
int button_new = 1;
int button_old = 1;
int elbow_tune = 0; //degrees
int elbow_tune2 = 0; //degrees
int level_tune = 10; //degrees
int wrist_tune = 10; //degrees

float x_velocity = 0;
float x_velocity_tune = 2; //tunes zeros of joystick
float y_velocity = 0;
float y_velocity_tune = -3; //tunes zeros of joystick
float global_velocity = 90;

int slow = 200; //slows speed of manipulator... similar to global_velocity

int loop_delay = 1; //mili second


void setup() {
  // put your setup code here, to run once:
  pinMode(button_pin, INPUT);
  pinMode(led_pin, OUTPUT);
  digitalWrite(button_pin, HIGH);
  Serial.begin(9600);

  elbow_servo.attach(9);
  level_servo.attach(10);
  wrist_servo.attach(11);

  //starting position of the manipulator
  elbow_servo.write(elbow_angle + elbow_tune);
  level_servo.write(180 - elbow_angle + level_tune);
  wrist_servo.write(wrist_angle + wrist_tune);

  delay(3000); //gives Devon time to do things before everything starts moving
  
}

void loop() {
//this section reads output of joystick and maps it to velocity
  x_velocity = map(analogRead(x_pin), 0, 1023, -global_velocity, global_velocity);
  y_velocity = map(analogRead(y_pin), 0, 1023, global_velocity, -global_velocity);

//this section disregards low velocities (less than 10% max). 
//keeps the manipulator from creeping should the joystick have non-zero zeros
 if (y_velocity >= -(global_velocity/10) and y_velocity <= (global_velocity/10)){
    y_velocity = 0;
  }
  if (x_velocity >= -(global_velocity/10) and x_velocity <= (global_velocity/10)){
    x_velocity = 0;
  }

//determines protocol based on [if] auto-leveling (chicken) is desired
// [else] doesn't move the elbow servos
  if (chicken == 0){
    elbow_angle = elbow_angle_old + y_velocity/(slow);
    level_angle = level_angle_old - y_velocity/(slow);
    wrist_angle = wrist_angle_old + x_velocity/(slow);
  }
  else {
    level_angle = level_angle_old + y_velocity/(slow);
    wrist_angle = wrist_angle_old + x_velocity/(slow);
  }

//keeps the velocites from overshooting 0 or 180 degrees
  if (elbow_angle >= 180){
    elbow_angle = 180;
  }
  if (elbow_angle <= 0){
    elbow_angle = 0;
  }
  if (level_angle >= 140){
    level_angle = 140;
  }
  if (level_angle <= 20){
    level_angle = 20;
  }
  if (wrist_angle >= 180){
    wrist_angle = 180;
  }
  if (wrist_angle <= 0){
    wrist_angle = 0;
  }

//always want to write thh wrist_servo
  wrist_servo.write(wrist_angle + wrist_tune);

//determines protocol depending on [if] auto-leveling (chicken)
//[else] only moves leveling servo
  if (chicken == 0){
    elbow_servo.write(elbow_angle + elbow_tune);
    elbow_servo2.write(180 - elbow_angle + elbow_tune2); //second servo moves in opposite direction
    level_servo.write(level_angle + level_tune);
  }
  else {
    level_servo.write(level_angle + level_tune);
  }

  //Serial.println(elbow_angle);
  //Serial.println(level_angle);

//save new positions to change during the next loop
  elbow_angle_old = elbow_angle;
  level_angle_old = level_angle;
  wrist_angle_old = wrist_angle;
  
  delay(loop_delay); //delay to smooth the servo. Unnecessary?


  //-------------HOLD CODE Start------------------//
  button_new = digitalRead(button_pin);
  if (button_new == 0) {
    if (button_old == 1) {
      chicken = 1;
      button_old = 0;
    }
    else {
      chicken = 0;
      button_old = 1;
    }
    delay(500); //delays to prevent multiple loops registering and toggling clicking before a single physical click is completed
  }

//turns on LED to signal if in auto-leveling (chicken) mode
  if (chicken == 1) {
    digitalWrite(led_pin, HIGH);
  }
  else {
    digitalWrite(led_pin, LOW);
  }
  //-------------HOLD CODE End-------------------// 
  
}

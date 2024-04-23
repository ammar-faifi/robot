#include <AccelStepper.h>
#include <Servo.h>


// Number of motors
const int numMotors = 6;

// Define motor pins
const int motorPins[numMotors][2] = {
  {2, 3},  // Motor 1: STEP pin 2, DIR pin 3
  {4, 5},  // Motor 2: STEP pin 4, DIR pin 5
  {6, 7},  // Motor 3: STEP pin 6, DIR pin 7
  {8, 9},  // Motor 4: STEP pin 8, DIR pin 9
  {10, 11}, // Motor 5: STEP pin 10, DIR pin 11
  {12, 13} // Motor 6: STEP pin 12, DIR pin 13
};

const int servoClosePosition = 0; // 5
const int servoOpenPosition = 180; // 165
const int servoPin = 14;
int pos = 5;
int servoCurrentPosition = 165; 
int servoRunning = 0;
#define WITHIN_BOUNDS(x) max(min((x), (servoOpenPosition)), (servoClosePosition))

Servo servo;
unsigned long lastServoMoveTime = 0;
const int servoSpeed = 10; // milliseconds between servo moves


// Create an array of AccelStepper objects
AccelStepper motors[numMotors] = {
  {1, motorPins[0][0], motorPins[0][1]},
  {1, motorPins[1][0], motorPins[1][1]},
  {1, motorPins[2][0], motorPins[2][1]},
  {1, motorPins[3][0], motorPins[3][1]},
  {1, motorPins[4][0], motorPins[4][1]},
  {1, motorPins[5][0], motorPins[5][1]}
};

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate
  // Initialize each motor
  for (int i = 0; i < numMotors; i++) {
    motors[i].setMaxSpeed(1000);
    motors[i].setAcceleration(500);
  }
  servo.attach(14); // Attach the servo on servoPin to the servo object
}

void loop() {
  //     int start = 5;
  //     int end = 165;
  // if (millis() - lastServoMoveTime > servoSpeed) {  // Goes from 0 degrees to 180 degrees
  //   myservo.write(pos++);        
  //   if (pos > end) {
  //     pos = end;
  //   } else if (pos < start) {
  //     pos = start; 
  //   }    // Tell servo to go to position in variable 'pos'
  //   lastServoMoveTime = millis();
  // }
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    executeMotorCommand(command);
  }

  // Continuously move motors that are running
  for (int i = 0; i < numMotors; i++) {
    motors[i].run();
  }
  moveServoGradually(servoRunning);
}

void executeMotorCommand(String command) {
  for (int i = 0; i < numMotors; i++) {
    String motorCommand = "M" + String(i+1);
    if (command.startsWith(motorCommand + "CW")) {
      motors[i].move(20000);  // Move motor i+1 clockwise
    } else if (command.startsWith(motorCommand + "CCW")) {
      motors[i].move(-20000); // Move motor i+1 counterclockwise
    } else if (command.startsWith(motorCommand + "STOP")) {
      motors[i].stop(); // Stop motor i+1
      // motors[i].disableOutputs(); // Optionally disable outputs to save power
    }
  }
  if (command == "M7C") { // Close the gripper
    servoRunning = 1;
  } else if (command == "M7O") { // Open the gripper
    servoRunning = 2;
  } else if (command == "M7S") { // Stop the gripper
    servoRunning = 0;
  }
}

void moveServoGradually(int state) {
  if (millis() - lastServoMoveTime > servoSpeed) {
    Serial.println(state);
    Serial.println(WITHIN_BOUNDS(servo.read() - 1));
    switch (state) {
      case 1: // M7C (Close the gripper)
        servo.write(WITHIN_BOUNDS(servo.read() - 1));
        break;
      case 2: // M7O (Open the gripper)
        servo.write(WITHIN_BOUNDS(servo.read() + 1));
        break;
      default:
        // No action needed if the servo is not moving
        break;
    }
    lastServoMoveTime = millis();
  }
}


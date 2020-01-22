#include <ArduinoJson.h>

class Metrics {
  public:
    //sensor readings
    int rightDistance, leftDistance, frontDistance;
    String labelRD = "rightDistance";
    String labelLD = "leftDistance";
    String labelFD = "frontDistance";

    //method that returns the distances in a json format
    String toString() {
      return ("{\"" + labelRD + "\":\"" + rightDistance + "\",\"" + labelLD + "\":\"" + leftDistance + "\",\"" + labelFD + "\":\"" + frontDistance + "\"}");
    };
};

// Input pins for motors. Side: Right/Left Cable Color: Red/Black
const int in_RR = 6 ;
const int in_RK = 9 ;
const int in_LR = 11 ;
const int in_LK = 10 ;

// define sensor pins t->trig e->echo
const int rightTPin = 2;
const int rightEPin = 3;
const int leftTPin = 7;
const int leftEPin = 8;
const int frontTPin = 4;
const int frontEPin = 5;

//define values for speed
const int high = 150;
const int low = 0;

const int capacity = 6 * JSON_OBJECT_SIZE(3);

Metrics *m = new Metrics();

//function to get input from a sensor
void getRightDistance() {
  // Clears the trigPin
  digitalWrite(rightTPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(rightTPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(rightTPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(rightEPin, HIGH);
  m->rightDistance = duration * 0.034 / 2;
}

void getLeftDistance() {
  // Clears the trigPin
  digitalWrite(leftTPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(leftTPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(leftTPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(leftEPin, HIGH);
  m->leftDistance = duration * 0.034 / 2;
}

void getFrontDistance() {
  // Clears the trigPin
  digitalWrite(frontTPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(frontTPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(frontTPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(frontEPin, HIGH);
  m->frontDistance = duration * 0.034 / 2;
}

//functions to control the car
void turnRight() {
  analogWrite(in_RR, low);
  analogWrite(in_RK, high);
  analogWrite(in_LK, low);
  analogWrite(in_LR, high);
}

void turnLeft() {
  analogWrite(in_RR, high);
  analogWrite(in_RK, low);
  analogWrite(in_LK, high);
  analogWrite(in_LR, low);
}

void forward() {
  analogWrite(in_RR, high) ;
  analogWrite(in_RK, low) ;
  analogWrite(in_LR, high) ;
  analogWrite(in_LK, low) ;
}

void brake() {
  analogWrite(in_RR, low) ;
  analogWrite(in_RK, low) ;
  analogWrite(in_LR, low) ;
  analogWrite(in_LK, low) ;
}

//function to receive command from raspberry pi
//command should be a string in json format {"code":"integer between 0-4"}
//code 0: forward
//code 1: turn right
//code 2: turn left
//code 3: turnAround !Need work
//code 4: brake
void getCommand() {
  String input;

  if (Serial.available() > 0) {
    input = Serial.readString();
    DynamicJsonDocument dict(capacity);
    DeserializationError err = deserializeJson(dict, input);
    int command = dict["code"].as<int>();
    if (command == 0) {
      forward();
    }
    else if (command == 1) {
      turnRight();
    }
    else if (command == 2) {
      turnLeft();
    }
    else if (command == 3) {
      //turnAround();
    }
    else {
      brake();
    }
  }
}

void setup() {
  pinMode(in_RR, OUTPUT) ; //Logic pins are also set as output
  pinMode(in_RK, OUTPUT) ;
  pinMode(in_LR, OUTPUT) ;
  pinMode(in_LK, OUTPUT) ;

  pinMode(rightTPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(rightEPin, INPUT); // Sets the echoPin as an Input
  pinMode(leftTPin, OUTPUT);
  pinMode(leftEPin, INPUT);
  pinMode(frontTPin, OUTPUT);
  pinMode(frontEPin, INPUT);
  Serial.begin(9600); // Starts the serial communication
}

void loop() {
  getRightDistance();
  getLeftDistance();
  getFrontDistance();
  Serial.println(m->toString());
  getCommand();
}

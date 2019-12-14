// Input pins for motors. Side: Right/Left Cable Color: Red/Black
const int in_RR = 6 ;
const int in_RK = 9 ;
const int in_LR = 11 ;
const int in_LK = 10 ;

// define sensor pins t->trig e->echo
const int rightTPin = 2;
const int rightEPin = 3;
const int frontTPin = 4;
const int frontEPin = 5;
const int leftTPin = 7;
const int leftEPin = 8;

// defines variables
long rightDuration, frontDuration, leftDuration;
int rightDistance, frontDistance, leftDistance;
//For providing logic to L298 IC to choose the direction of the DC motor

void getRightDistance()
{
  // Clears the trigPin
  digitalWrite(rightTPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(rightTPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(rightTPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  rightDuration = pulseIn(rightEPin, HIGH);
  // Calculating the distance
  rightDistance = rightDuration * 0.034 / 2;
}
void getFrontDistance()
{
  // Clears the trigPin
  digitalWrite(frontTPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(frontTPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(frontTPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  frontDuration = pulseIn(frontEPin, HIGH);
  // Calculating the distance
  frontDistance = frontDuration * 0.034 / 2;
}
void getLeftDistance()
{
  // Clears the trigPin
  digitalWrite(leftTPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(leftTPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(leftTPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  leftDuration = pulseIn(leftEPin, HIGH);
  // Calculating the distance
  leftDistance = leftDuration * 0.034 / 2;
}

void turnR()
{
  //TURN LIKE TANK clockwise
  digitalWrite(in_RR, LOW) ;
  digitalWrite(in_RK, HIGH) ;
  digitalWrite(in_LK, LOW) ;
  digitalWrite(in_LR, HIGH) ;
}

void turnL()
{
  //TURN LIKE TANK clockwise
  digitalWrite(in_RR, HIGH) ;
  digitalWrite(in_RK, LOW) ;
  digitalWrite(in_LK, HIGH) ;
  digitalWrite(in_LR, LOW) ;
}
void forward()
{
  //FORWARD
  digitalWrite(in_RR, HIGH) ;
  digitalWrite(in_RK, LOW) ;
  digitalWrite(in_LR, HIGH) ;
  digitalWrite(in_LK, LOW) ;
}
void brake()
{
  //For brake
  digitalWrite(in_RR, LOW) ;
  digitalWrite(in_RK, LOW) ;
  digitalWrite(in_LR, LOW) ;
  digitalWrite(in_LK, LOW) ;
}

void setup()
{
  pinMode(in_RR, OUTPUT) ; //Logic pins are also set as output
  pinMode(in_RK, OUTPUT) ;
  pinMode(in_LR, OUTPUT) ;
  pinMode(in_LK, OUTPUT) ;

  pinMode(rightTPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(rightEPin, INPUT); // Sets the echoPin as an Input
  pinMode(frontTPin, OUTPUT);
  pinMode(frontEPin, INPUT);
  pinMode(leftTPin, OUTPUT);
  pinMode(leftEPin, INPUT);
  Serial.begin(9600); // Starts the serial communication
}

void loop()
{
  getRightDistance();
  Serial.print("Right sensor distance: ");
  Serial.print(rightDistance);
  Serial.println(" cm");

  getFrontDistance();
  Serial.print("Front sensor distance: ");
  Serial.print(frontDistance);
  Serial.println(" cm");

  getLeftDistance();
  Serial.print("Left sensor distance: ");
  Serial.print(leftDistance);
  Serial.println(" cm");

  if (frontDistance > 8) {
    forward();
    Serial.println("Going forward");
  }
  else {
    brake();
    if (rightDistance > 20){
      turnR();
      Serial.println("Turning right >");
    }
    else if (leftDistance > 20){
      turnL();
      Serial.println("Turning left <");
    }
  }

}

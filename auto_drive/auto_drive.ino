const int in_1 = 6 ;
const int in_2 = 9 ;
const int in_3 = 11 ;
const int in_4 = 10 ;

// defines pins numbers t->trig e->echo
const int t1Pin = 2;
const int e1Pin = 3;
const int t2Pin = 4;
const int e2Pin = 5;
const int t3Pin = 7;
const int e3Pin = 8;

// defines variables
long duration1,duration2,duration3;
int distance1,distance2,distance3;
//For providing logic to L298 IC to choose the direction of the DC motor 

void d1()
{
    // Clears the trigPin
    digitalWrite(t1Pin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(t1Pin, HIGH);
    delayMicroseconds(10);
    digitalWrite(t1Pin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration1 = pulseIn(e1Pin, HIGH);
    // Calculating the distance
    distance1= duration1*0.034/2;
    // Prints the distance on the Serial Monitor
}
void d2()
{
    // Clears the trigPin
    digitalWrite(t2Pin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(t2Pin, HIGH);
    delayMicroseconds(10);
    digitalWrite(t2Pin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration2 = pulseIn(e2Pin, HIGH);
    // Calculating the distance
    distance2= duration2*0.034/2;
    // Prints the distance on the Serial Monitor
}
void d3()
{
    // Clears the trigPin
    digitalWrite(t3Pin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(t3Pin, HIGH);
    delayMicroseconds(10);
    digitalWrite(t3Pin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration3 = pulseIn(e3Pin, HIGH);
    // Calculating the distance
    distance3= duration3*0.034/2;
    // Prints the distance on the Serial Monitor
}

void turnR()
{
    //TURN LIKE TANK clockwise
    digitalWrite(in_1,LOW) ;
    digitalWrite(in_2,HIGH) ;
    digitalWrite(in_4,LOW) ;
    digitalWrite(in_3,HIGH) ;
}

void turnL()
{
    //TURN LIKE TANK clockwise
    digitalWrite(in_1,HIGH) ;
    digitalWrite(in_2,LOW) ;
    digitalWrite(in_4,HIGH) ;
    digitalWrite(in_3,LOW) ;
}
void forward()
{
    //FORWARD
    digitalWrite(in_1,HIGH) ;
    digitalWrite(in_2,LOW) ;
    digitalWrite(in_3,HIGH) ;
    digitalWrite(in_4,LOW) ;
    delay(1000) ;
}
void brake()
{
    //For brake
    digitalWrite(in_1,LOW) ;
    digitalWrite(in_2,LOW) ;
    digitalWrite(in_3,LOW) ;
    digitalWrite(in_4,LOW) ;
}

void setup()
{
pinMode(in_1,OUTPUT) ;  //Logic pins are also set as output
pinMode(in_2,OUTPUT) ;
pinMode(in_3,OUTPUT) ;
pinMode(in_4,OUTPUT) ;

pinMode(t1Pin, OUTPUT); // Sets the trigPin as an Output
pinMode(e1Pin, INPUT); // Sets the echoPin as an Input
pinMode(t2Pin, OUTPUT);
pinMode(e2Pin, INPUT);
pinMode(t3Pin, OUTPUT);
pinMode(e3Pin, INPUT);
Serial.begin(9600); // Starts the serial communication
}

void loop()
{




forward();   
delay(1000) ;
  
brake();
delay(100);
turnL();
delay(3000) ;

forward();
delay(1000) ;   

brake();
delay(100);
turnR();  
delay(3000) ;

Serial.print("Distance: ");
d1();
Serial.print(distance1);
Serial.println(" cm");

d2();
Serial.print("Distance: ");
Serial.print(distance2);
Serial.println(" cm");

d3();
Serial.print("Distance: ");
Serial.print(distance3);
Serial.println(" cm");

}

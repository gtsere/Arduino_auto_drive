const int pwm = 2 ;  //initializing pin 2 as pwm
const int in_1 = 6 ;
const int in_2 = 9 ;
const int in_3 = 11 ;
const int in_4 = 10 ;

//For providing logic to L298 IC to choose the direction of the DC motor 

void setup()
{
pinMode(pwm,OUTPUT) ;   //we have to set PWM pin as output
pinMode(in_1,OUTPUT) ;  //Logic pins are also set as output
pinMode(in_2,OUTPUT) ;
pinMode(in_3,OUTPUT) ;
pinMode(in_4,OUTPUT) ;
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
void loop()
{

//digitalWrite(in_1,HIGH) ;
//digitalWrite(in_2,LOW) ;
//digitalWrite(in_3,HIGH) ;
//digitalWrite(in_4,LOW) ;
//analogWrite(pwm,255) ;
//
///*setting pwm of the motor to 255
//we can change the speed of rotaion by chaning pwm input but we are only
//using arduino so we are using higest value to driver the motor  */
//

analogWrite(pwm,255) ;

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



 }

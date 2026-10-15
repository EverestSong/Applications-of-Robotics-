int correction = 0;

// Right motor
const int In1 = 10;
const int In2 = 11; 

// Left motor
const int In3 = 8;
const int In4 = 9; 

const int EnA = 6; 
const int EnB = 5; 

const int velocity = 100;
const float multiplier = 10;

void setup()
{
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  
  pinMode(EnA, OUTPUT); 
  pinMode(EnB, OUTPUT);
  
  Serial.begin(9600);
  steer(0, 150);
  delay(1000);
}

void loop()
{
  if (Serial.available()) {
    String message = Serial.readStringUntil('\n');
    correction = message.toInt();
      
    if (correction > 0) {
        Serial.println("Move to the right");
      }
  
    else if (correction < 0) {
        Serial.println("Move to the left");
    }
    
    steer(correction, velocity);
  }

  else {
    
  }
}

void goStraight(int rightSpeed, int leftSpeed) {
  // Turn on motor (right)
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);

  // Turn on motor (left)
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);

  analogWrite(EnA, rightSpeed); 
  analogWrite(EnB, leftSpeed);
} 

void steer(int correction, int speed) {
  int amount = correction * multiplier;
  int leftSpeed = speed + amount;
  int rightSpeed = speed - amount;

  leftSpeed = constrain(leftSpeed, 0, 255);
  rightSpeed = constrain(rightSpeed, 0, 255);

  goStraight(rightSpeed, leftSpeed);
}

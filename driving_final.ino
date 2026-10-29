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
int correction = 0;
bool isStopped = false;


void setup()
{
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);
  pinMode(In3, OUTPUT);
  pinMode(In4, OUTPUT);
  pinMode(EnA, OUTPUT); 
  pinMode(EnB, OUTPUT);
  
  Serial.begin(115200);
  Serial.setTimeout(50);
  steer(0, 150);
  delay(1000);
}

void loop()
{
  if (Serial.available()) {
    String message = Serial.readStringUntil('\n');

    // Steering correction
    if (isStopped == false) {
      correction = message.toInt();
      steer(correction, velocity);

      if (correction > 0) {
        Serial.println("Move to the right");
      }
  
      else if (correction < 0) {
          Serial.println("Move to the left");
      }
    }

    // STOP command
    if (message == "STOP") {
      isStopped = true;
      stop();
      Serial.println("Stop");
    }
    
    // GO command
    else if (message == "GO") {
      isStopped = false;
      steer(correction, velocity);
      Serial.println("Go");
    }   
  }
}

void goStraight(int rightSpeed, int leftSpeed) {
  // Turn on motor (right)
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);

  // Turn on motor (left)
  digitalWrite(In3, HIGH);
  digitalWrite(In4, LOW);

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

void stop()
{
  // Disable both motors
  analogWrite(EnA, 0);
  analogWrite(EnB, 0);

  digitalWrite(In1, LOW);
  digitalWrite(In2, LOW);
  digitalWrite(In3, LOW);
  digitalWrite(In4, LOW);
}

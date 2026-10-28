// Ultrasonic sensor 
const int echoPin = 6;
const int trigPin = 7;

// RGB LED module (turn signals)
int ledPins[2][3] = {{8, 9, 10}, {11, 12, 13}};
enum Side {LEFT, RIGHT};
bool indicatorOn = false;

// For millis()
const unsigned long ultrasonicInterval = 100;
unsigned long previousUltrasonicTime = 0;
const unsigned long indicatorInterval = 500;
unsigned long previousIndicatorTime = 0;

void setup() {
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);

  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 3; j++) {
      pinMode(ledPins[i][j], OUTPUT);
    }
  }

  Serial.begin(9600);
}

void loop() {
  unsigned long currentTime = millis();

  if (currentTime - previousUltrasonicTime >= ultrasonicInterval) {
    float distance = ultrasonicSensorDistance();
    Serial.print(String(distance) + " cm\n");
    previousUltrasonicTime = currentTime;
  }

  indicate(RIGHT); 
}

float ultrasonicSensorDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPin, LOW);

  float duration = pulseIn(echoPin, HIGH);
  float distance = microsecondsToCentimeters(duration);

  return distance;
}

float microsecondsToCentimeters(float microseconds)
{
  // Since distance = (speed * time) / 2 
  return microseconds * 0.0343 / 2;
}

void setColor(int red, int green, int blue, Side side) {
  analogWrite(ledPins[side][0], red);
  analogWrite(ledPins[side][1], green);
  analogWrite(ledPins[side][2], blue);
}

void indicate(Side side) {
  unsigned long currentTime = millis();

  if (currentTime - previousIndicatorTime >= indicatorInterval) {
    indicatorOn = !indicatorOn;

    if (indicatorOn) {
      setColor(255, 130, 54, side);
    }

    else {
      setColor(0, 0, 0, side);
    }

    previousIndicatorTime = currentTime;
  }
}

const int echoPin = 6;
const int trigPin = 7;

const unsigned long sensorInterval = 100;
unsigned long previousSensorTime = 0;

void setup() {
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  unsigned long currentSensorTime = millis();

  if (currentSensorTime - previousSensorTime >= sensorInterval) {
    float distance = ultrasonicSensorDistance();
    Serial.print(distance);
    Serial.print(" cm");
    Serial.println();  
    previousSensorTime = currentSensorTime;
  }
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

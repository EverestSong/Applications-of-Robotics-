const int echoPin = 8;
const int trigPin = 9;

void setup() {
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  // duration: Duration of ping (μs)
  // distance: The distance (cm)
  long duration, distance;

  // The PING is triggered by a HIGH pulse of 2 or more μs.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);

  // Convert the time into a distance
  distance = microsecondsToCentimeters(duration);
  
  Serial.print(distance);
  Serial.print(" cm");
  Serial.println();  
  delay(100);
}

long microsecondsToCentimeters(long microseconds)
{
  return microseconds / 29 / 2;
}

const int green = 2;
const int yellow = 3;
const int red = 4;

int greenDuration = 10000;
int yellowDuration = 4000;
int redDuration = 10000;

void setup() {
  pinMode(green, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(red, OUTPUT);
}

void loop() {
  cycle();
}

void cycle() {
  digitalWrite(green, HIGH);
  delay(greenDuration);
  digitalWrite(green, LOW);

  digitalWrite(yellow, HIGH);
  delay(yellowDuration);
  digitalWrite(yellow, LOW);

  digitalWrite(red, HIGH);
  delay(redDuration);
  digitalWrite(red, LOW);
}

const int green = 2;
const int yellow = 3;
const int red = 4;

const unsigned long greenDuration = 5000;
const unsigned long yellowDuration = 4000;
const unsigned long redDuration = 5000;

unsigned long previousLightTime = 0;

enum TrafficLightState {
  GREEN,
  YELLOW,
  RED
};

TrafficLightState currentState = GREEN;

void setup() {
  pinMode(green, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(red, OUTPUT);

  setLights(HIGH, LOW, LOW);
}

void loop() {
  cycle();
}

void cycle() {
  unsigned long currentTime = millis();

  switch (currentState) {
    case GREEN:
      if (currentTime - previousLightTime >= greenDuration) {
        setLights(LOW, HIGH, LOW);

        currentState = YELLOW;
        previousLightTime = currentTime;
      }
      break;

    case YELLOW:
      if (currentTime - previousLightTime >= greenDuration) {
        setLights(LOW, LOW, HIGH);

        currentState = RED;
        previousLightTime = currentTime;
      }
      break;

    case RED:
      if (currentTime - previousLightTime >= greenDuration) {
        setLights(HIGH, LOW, LOW);

        currentState = GREEN;
        previousLightTime = currentTime;
      }
      break;
  }
}

void setLights(bool greenState, bool yellowState, bool redState) {
  digitalWrite(green, greenState);
  digitalWrite(yellow, yellowState);
  digitalWrite(red, redState);
}

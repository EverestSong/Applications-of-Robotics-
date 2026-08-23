int ledPins[2][3] = {{8, 9, 10}, {11, 12, 13}};

enum Side {
  LEFT,
  RIGHT
};

const unsigned long indicatorInterval = 500;
unsigned long previousIndicatorTime = 0;
bool indicatorOn = false;

void setup() {
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 3; j++) {
      pinMode(ledPins[i][j], OUTPUT);
    }
  }
}

void loop() {
  indicate(LEFT); 
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

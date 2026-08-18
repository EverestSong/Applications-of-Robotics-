int redPinLeft = 8;
int greenPinLeft = 9;
int bluePinLeft = 10;

int redPinRight = 11;
int greenPinRight = 12;
int bluePinRight = 13;

void setup() {
  pinMode(redPinLeft, OUTPUT);
  pinMode(greenPinLeft, OUTPUT);
  pinMode(bluePinLeft, OUTPUT);

  pinMode(redPinRight, OUTPUT);
  pinMode(greenPinRight, OUTPUT);
  pinMode(bluePinRight, OUTPUT);
}

void loop() {
  indicate("right"); 
}

void setColor(int red, int green, int blue, String signal) {
  if (signal == "left") {
    analogWrite(redPinLeft, red);
    analogWrite(greenPinLeft, green);
    analogWrite(bluePinLeft, blue);
  }

  if (signal == "right") {
    analogWrite(redPinRight, red);
    analogWrite(greenPinRight, green);
    analogWrite(bluePinRight, blue);
  }
}

void indicate(String signal) {
  if (signal == "left") {
    setColor(255, 130, 54, "left"); 
    delay(500); 
    setColor(0, 0, 0, "left"); 
    delay(500);
  }

  if (signal == "right") {
    setColor(255, 130, 54, "right"); 
    delay(500); 
    setColor(0, 0, 0, "right"); 
    delay(500);
  }
}

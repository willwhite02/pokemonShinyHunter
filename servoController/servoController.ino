#include <Servo.h>

Servo leftServo;
Servo rightServo;

void setup() {
  Serial.begin(9600);

  leftServo.attach(2);
  rightServo.attach(3);

  leftServo.write(90);
  rightServo.write(90);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == 'L') {
      leftServo.write(180);
      delay(200);
      leftServo.write(90);
    }

    if (cmd == 'R') {
      rightServo.write(0);
      delay(200);
      rightServo.write(90);
    }
  }
}
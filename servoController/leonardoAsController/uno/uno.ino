#include <SoftwareSerial.h>

// RX, TX
SoftwareSerial leonardoSerial(10, 11);

void setup() {
  Serial.begin(9600);          // Laptop ↔ Uno
  leonardoSerial.begin(9600);  // Uno → Leonardo
}

void loop() {
  while (Serial.available() > 0) {
    char command = Serial.read();
    leonardoSerial.write(command);
  }
}
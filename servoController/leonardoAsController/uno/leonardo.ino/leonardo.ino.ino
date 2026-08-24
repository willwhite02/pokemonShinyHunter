void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial1.begin(9600);
}

void loop() {
  if (Serial1.available() > 0) {
    char command = Serial1.read();

    if (command == 'T') {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}
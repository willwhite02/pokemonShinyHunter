#include <NintendoSwitchControlLibrary.h>

const unsigned long BUTTON_TIME = 150;
const unsigned long HAT_TIME = 150;

// Send harmless inputs while the Switch recognizes the controller.
void reconnectController() {
  pushButton(Button::L, 500, 5);
}

void setup() {
  // Commands arrive from the Uno:
  // Uno D11 (TX) -> Leonardo D0 (RX)
  Serial1.begin(9600);

  // Automatically reconnect when the Leonardo powers up.
  reconnectController();
}

void resetGame() {
  // Go to HOME
  pushButton(Button::HOME, 150);
  delay(1200);

  // Close software
  pushButton(Button::X, 150);
  delay(1000);

  // Confirm
  pushButton(Button::A, 150);
  delay(1000);
}

void loop() {
  if (Serial1.available() <= 0) {
    return;
  }

  char command = Serial1.read();

  switch (command) {
    // reconnect controller
    case 'c':
      reconnectController();
      break;

    // press a
    case 'a':
      pushButton(Button::A, BUTTON_TIME);
      break;
    
    // perform entire reset sequence
    case 'r':
      resetGame();
      break;

    default:
      // Ignore newlines and unsupported characters.
      break;
  }
}
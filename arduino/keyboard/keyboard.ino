#include "Keyboard.h"

const int PRESS = 1;
const int RELEASE = 2;
//int TYPE = 1;

void setup() { 
  // open the serial port:
  Serial.begin(9600);
  // initialize control over the keyboard:
  Keyboard.begin();
}

void loop() {
  // check for incoming serial data:
  if (Serial.available() > 0) {
    // read incoming serial data
    // data should be 3 bytes: [character, press/release byte, null]
    byte input[3];
    Serial.readBytesUntil(0, input, 3);
    char character = input[0];
    switch (input[1]) {
      case PRESS:
        Keyboard.press(character);
        break;
       case RELEASE:
        Keyboard.release(character);
        break;
    }
  }
}

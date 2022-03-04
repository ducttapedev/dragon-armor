#include <Keyboard.h>

const int PRESS = 1;
const int RELEASE = 2;
const int TYPE = 3;
const int MAX_COMMANDS = 500;

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
    byte input[2 * MAX_COMMANDS + 1];
    int length = Serial.readBytesUntil(0, input, 2 * MAX_COMMANDS + 1);

    int index = 0;
    for(int i = 0; i < length; i+= 2) {
  //    char s[3];
  //    snprintf(s, 3, "%d", input);
      Serial.print("0x");
      Serial.print(input[i], HEX);
      Serial.print(",0x");
      Serial.println(input[i + 1], HEX);
      
      char character = input[i];
      switch (input[i + 1]) {
        case PRESS:
          Keyboard.press(character);
          break;
         case RELEASE:
          Keyboard.release(character);
          break;
         case TYPE:
          Keyboard.write(character);
          break;       
      }
    }
  }
}

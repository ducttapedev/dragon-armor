# Dragon Armor
This mini-project enables Dragon to send real hardware keystrokes via USB that should be indistinguishable from a normal keyboard. You can also send keystrokes from one computer with Dragon installed to another computer without. It is built on top of the [Caster](https://github.com/dictation-toolbox/Caster) project, which is itself built on the [Dragonfly](https://github.com/dictation-toolbox/dragonfly) framework. It currently does not depend on any Caster files so it should theoretically work on just Dragonfly, although I have not verified this (please modify this readme if you do).|

## Motivation
Caster, Dragonfly, and [Natlink](https://github.com/dictation-toolbox/natlink) have been incredibly useful for those who wish to reduce keyboard usage and those with disabilities that cannot use a normal keyboard, myself included. However, because a virtual keyboard is used, they don't work properly or at all in some situations (e.g. VMware). By sending keystrokes via USB that are indistinguishable from a real keyboard, it should work with all programs.

This also enables you to have one copy of Dragon control multiple computers, so that you don't have to  reconfigure and retrain Dragon on each of your computers. Yes, you can export and import profiles, but they will inevitably get out of sync if you switch frequently between computers. Furthermore, not everything gets transferred, such as pronunciations.

## Limitations
Only commands are sent through the Arduino. Dictation is still processed normally by Dragon. If you are outputting keystrokes to a different computer from the one that Dragon is installed on, you will only be able to send commands and not dictation. Same goes if you are using a program like VMware that normally does not work with Dragon. This is because dictation does not go through Dragonfly. However, you can "convert" dictation into a command by prepending it with "say" "slip" or "cop."

The goal is to also have an option to send Dragon dictation via the Arduino, but it will probably require full keyboard control. In that case, you would need a dedicated machine or VM that just runs Dragon, but that probably won't be a problem because if you don't have an additional machine or VMs, you can just disable this option and everything should still work. Only one process can communicate with the serial port at a time so the implementation will require interprocess communication.

## Requirements
- Unfortunately, this does require an Arduino. Currently the only one I have verified as working is the [Arduino Due](https://store.arduino.cc/arduino-due) ([sometimes cheaper here](https://www.amazon.com/Arduino-org-A000062-Arduino-Due/dp/B00A6C3JN2)). I am not sure if any others will work but please add to this readme if you find any that do.
- [Dragonfly](https://github.com/dictation-toolbox/dragonfly) and possibly [Caster](https://github.com/dictation-toolbox/Caster)
- `pip install pyserial`

## Installation
1. Download the [Arduino IDE](https://www.arduino.cc/en/software)
2. Connect the Arduino programming port to your computer via USB and the other port to the target computer via USB, which can be the same computer. If you are not sure, just connect both ports to your computer. The Arduino IDE should make it clear which port is which.
3. Launch the Arduino IDE. It may prompt you to install libraries for your Arduino device. Make sure to install those libraries as well as the Keyboard library. You can see a list of libraries for installation and updating in Tools > Manage Libraries. You may need to Arduino IDE after this
4. Go to Tools > Port and select the port with "Programming Port" in its name
5. Go to Tools > Board > Arduino ARM (32-bit) Boards > Arduino Due (Programming Port)
6. Go to File > Open and open the `keyboard/keyboard.ino` file in this repository
7. Click on the upload button in the top left (a rightward pointing arrow) to upload your code onto the Arduino
8. Replace the `$castor_installation_directory/castervoice/__init__.py` file in your Caster installation with the file in the same path in this repository

Now you can launch Dragon and all commands will be sent as hardware keyboard strokes to the output port on the Arduino. It is easier to verify if the output is on a different computer.

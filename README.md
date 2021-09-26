# Dragon Armor
This mini-project enables Dragon to send real hardware keystrokes via USB that should be indistinguishable from a normal keyboard. You can also send keystrokes from one computer with Dragon installed (the "input" machine) to another computer (the "output" machine) without. It is built on top of the [Caster](https://github.com/dictation-toolbox/Caster) project, which is itself built on the [Dragonfly](https://github.com/dictation-toolbox/dragonfly) framework. It currently does not depend on any Caster files so it should theoretically work on just Dragonfly, although I have not verified this (please modify this readme if you do).|

## Motivation
Caster, Dragonfly, and [Natlink](https://github.com/dictation-toolbox/natlink) have been incredibly useful for those who wish to reduce keyboard usage and those with disabilities that cannot use a normal keyboard, myself included. However, because a virtual keyboard is used, they don't work properly or at all in some situations (e.g. VMware). By sending keystrokes via USB that are indistinguishable from a real keyboard, it should work with all programs.

This also enables you to have one copy of Dragon control multiple computers, so that you don't have to  reconfigure and retrain Dragon on each of your computers. Yes, you can export and import profiles, but they will inevitably get out of sync if you switch frequently between computers. Furthermore, not everything gets transferred, such as pronunciations.

## Limitations
### Dictation
Currently, I have not figured out an elegant way to send dictation directly to the Arduino (dragonfly commands work fine, provided they are keyboard only). This might be possible with dragonfly observers, but I have not been able to make it work with Dragon's formatting. [See here](https://github.com/michaelscheung/dragon-armor/blob/349b40ffad6cc3ac2cd6820aa5f8e0345acc72f5/_dragon_observer.py) for an initial attempt that was somewhat working. Because it did not properly preserve Dragon's formatting (e.g. for numbers), it was abandoned in favor of a more hacky approach using `getch`. If this can be made to work, we can probably get rid of the separate `arduino/run.bat` file that needs to be run and have everything automatically launch with dragonfly.

If your input and output machines are different, I have a workaround using Python's `getch` and focusing Dragon on the `arduino/run.bat` process, so that every dictation keystroke is captured by the program. Since this is a separate process from Dragon/dragonfly, we use interprocess communication to send commands from dragonfly to `arduino/run.bat` (dragonfly commands can be elegantly captured and sent to the Arduino without using the `getch` hack). `arduino/run.bat` sends both direct dictation and dragonfly commands received via interprocess communication to the Arduino. Dictation stops working if the `arduino/run.bat` process is no longer focused.

If your input and output machines are the same, Dragon functions normally as the dictation is not redirected anywhere. You will still be unable to send dictation to programs that don't work with Dragon's virtual keyboard, like VMware. However, you will now be able to send commands whereas before no interaction at all was possible. (You can also "convert" dictation into a command by prepending it with "say" "slip" or "cop.")

### Keyboard Only
Currently, only keyboard output is supported. Mouse commands don't work yet

### Context Awareness
Context aware commands don't work if the input and output computers are different. This should theoretically be possible with a process on the output machine that sends the current focused program to the input machine, but for now you will have to make the commands `CCRType.GLOBAL` and keep them always on or enable/disable them manually. For instance, the JetBrains Caster rule can be made global with the following modification to jetbrains.py, which can be done in the Caster user directory (usually AppData/Local/caster):
```
def get_rule():
    details = RuleDetails(ccrtype=CCRType.GLOBAL)
    return JetBrains, details
```

### Miscellaneous 
When Dragon armor is first started, you may have to send dictation through `arduino/run.bat` to make commands work (simply saying "testing" should work). This also sometimes happens randomly. This issue is probably due to some process hanging (perhaps `getch` is hogging the GIL?) and I imagine it should be fixable.

## Requirements
- Unfortunately, this does require an Arduino and 2 micro USB cables to connect it to the host computer and the receiving computer (which can be the same as the host). Currently the only one I have verified as working is the [Arduino Due](https://store.arduino.cc/arduino-due) ([sometimes cheaper here](https://www.amazon.com/Arduino-org-A000062-Arduino-Due/dp/B00A6C3JN2)). I am not sure if any others will work but please add to this readme if you find any that do. Raspberry Pi probably also works, but again I have not verified it.
- [Dragonfly](https://github.com/dictation-toolbox/dragonfly) and possibly [Caster](https://github.com/dictation-toolbox/Caster)
- `pip install pyserial`
- If you want the input machine to be a virtual machine, VMware seems to work better than Virtual Box. Virtual Box seems to be much slower to send data to the Arduino, and more prone to having issues requiring program restart.

## Installation
1. Download the [Arduino IDE](https://www.arduino.cc/en/software)
2. Connect the Arduino programming port to your computer via USB and the other port to the target computer via USB, which can be the same computer. If you are not sure, just connect both ports to your computer. The Arduino IDE should make it clear which port is which.
3. Launch the Arduino IDE. It may prompt you to install libraries for your Arduino device. Make sure to install those libraries as well as the Keyboard library. You can see a list of libraries for installation and updating in Tools > Manage Libraries. You may need to Arduino IDE after this
4. Go to Tools > Port and select the port with "Programming Port" in its name
5. Go to Tools > Board > Arduino ARM (32-bit) Boards > Arduino Due (Programming Port)
6. Go to File > Open and open the `keyboard/keyboard.ino` file in this repository
7. Click on the upload button in the top left (a rightward pointing arrow) to upload your code onto the Arduino
8. Clone the repo to your caster or dragonfly installation directory (e.g. Documents/Caster). Dragonfly will automatically load the files starting with "_" in the root directory.

## Run
1. Launch `arduino/run.bat`. This process receives commands as direct input and from dragonfly, and sends them to the Arduino.
2. Now you can launch Dragon and all commands will be sent as hardware keyboard strokes to the output port on the Arduino.
3. If your input and output computers are different, the input computer should focus the `arduino/run.bat` so that it can capture all dictation. Note that if this process is not focused, dictation won't work but commands still will

## Resilience
- If `arduino/run.bat` says that it has lost interprocess communication, it will try to automatically reconnect. Sometimes you have to send dictation and commands for it to realize it has been disconnected. If this still doesn't work, close and relaunch `arduino/run.bat`
- If `arduino/run.bat` says that it has lost connection to the Arduino, close and relaunch `arduino/run.bat`
- If there are still issues, close both `arduino/run.bat` and Dragon and relaunch everything (follow the instructions in the "Run" section)

## Contribution
Contributions are welcome; feel free to submit issues and pull requests. I hang out on the dictation-toolbox gitters (e.g. [Caster](https://gitter.im/dictation-toolbox/Caster), [Dragonfly](https://gitter.im/dictation-toolbox/dragonfly)), so feel free to reach out to me there. You can also e-mail me at the email address [here in the top right](https://github.com/michaelscheung/resume/blob/master/Michael%20Cheung%20Resume.pdf) (not listed here directly to prevent spam scrapers).

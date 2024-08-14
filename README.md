# TM1650

### 7 segment display driver for JY-MCU module based on TM1650 chip

##### Copyright (c) 2015 Anatoli Arkhipenko

[![arduino-library-badge](https://www.ardu-badge.com/badge/TM1650.svg?)](https://www.ardu-badge.com/TM1650)

### Python Version for Raspberry Pi

This library has been ported to Python and can be used on a Raspberry Pi. The Python version uses the `smbus` library for I2C communication.

#### Installation

To install the required `smbus` library, run the following command:

```bash
sudo apt-get install python3-smbus
```

#### Usage

Here is an example of how to use the Python version of the TM1650 library on a Raspberry Pi:

```python
import time
from TM1650 import TM1650

d = TM1650()

def setup():
    d.init()
    print("TM1650 Example Code")

def loop():
    d.displayOff()
    d.displayString("____")
    d.setBrightness(TM1650.MIN_BRIGHT)
    d.displayOn()
    time.sleep(0.1)
    line = "1234"

    d.displayString(line)
    d.setBrightnessGradually(TM1650.MAX_BRIGHT)
    time.sleep(2)
    d.setBrightnessGradually(TM1650.MIN_BRIGHT)
    d.displayOff()
    time.sleep(1)

    line = line[:1] + chr(ord(line[1]) | 128) + line[2:]
    d.displayOn()
    d.setBrightnessGradually(TM1650.MAX_BRIGHT)
    d.displayString(line)
    time.sleep(2)

    d.displayString("abcd")
    time.sleep(2)

    d.displayString("789 ")
    time.sleep(2)

    if d.displayRunning("1234567890abcdefghijklmnop"):
        while d.displayRunningShift():
            time.sleep(0.5)
    time.sleep(2)

    for i in range(20):
        d.displayOff()
        time.sleep(0.2)
        d.displayOn()
        time.sleep(0.2)

    for i in range(20):
        d.setBrightness(1)
        time.sleep(0.2)
        d.setBrightness(7)
        time.sleep(0.2)

    for i in range(20):
        for j in range(4):
            d.setDot(j, True)
            time.sleep(0.2)
        for j in range(4):
            d.setDot(j, False)
            time.sleep(0.2)

if __name__ == "__main__":
    setup()
    while True:
        loop()
```

###### Changelog:

v1.0.0:

- 2015-02-24 - Initial release 

v1.0.1:  

- 2015-04-27 - Added support of program memery (PROGMEM) to store the ASCII to Segment Code table

v1.0.2

- 2015-08-08 - Added check if panel is connected during init. All calls will be disabled is panel was not connected during init.

v1.1.0:

- 2015-12-20 - Code clean up. Moved to a single header file. Added Gradual brightness method


import time
import smbus
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

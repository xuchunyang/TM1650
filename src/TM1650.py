import smbus
import time

TM1650_DISPLAY_BASE = 0x34
TM1650_DCTRL_BASE = 0x24
TM1650_NUM_DIGITS = 16
TM1650_MAX_STRING = 128

TM1650_BIT_ONOFF = 0b00000001
TM1650_MSK_ONOFF = 0b11111110
TM1650_BIT_DOT = 0b00000001
TM1650_MSK_DOT = 0b11110111
TM1650_BRIGHT_SHIFT = 4
TM1650_MSK_BRIGHT = 0b10001111
TM1650_MIN_BRIGHT = 0
TM1650_MAX_BRIGHT = 7

TM1650_CDigits = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x82, 0x21, 0x00, 0x00, 0x00, 0x00, 0x02, 0x39, 0x0F, 0x00, 0x00, 0x00, 0x40, 0x80, 0x00,
    0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7f, 0x6f, 0x00, 0x00, 0x00, 0x48, 0x00, 0x53,
    0x00, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71, 0x6F, 0x76, 0x06, 0x1E, 0x00, 0x38, 0x00, 0x54, 0x3F,
    0x73, 0x67, 0x50, 0x6D, 0x78, 0x3E, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x39, 0x00, 0x0F, 0x00, 0x08,
    0x63, 0x5F, 0x7C, 0x58, 0x5E, 0x7B, 0x71, 0x6F, 0x74, 0x02, 0x1E, 0x00, 0x06, 0x00, 0x54, 0x5C,
    0x73, 0x67, 0x50, 0x6D, 0x78, 0x1C, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x39, 0x30, 0x0F, 0x00, 0x00
]

class TM1650:
    def __init__(self, aNumDigits=4):
        self.iNumDigits = min(aNumDigits, TM1650_NUM_DIGITS)
        self.iPosition = None
        self.iActive = False
        self.iBrightness = TM1650_MAX_BRIGHT
        self.iString = [''] * (TM1650_MAX_STRING + 1)
        self.iBuffer = [0] * (TM1650_NUM_DIGITS + 1)
        self.iCtrl = [0] * TM1650_NUM_DIGITS
        self.bus = smbus.SMBus(1)

    def init(self):
        self.iPosition = None
        for i in range(self.iNumDigits):
            self.iBuffer[i] = 0
            self.iCtrl[i] = 0
        try:
            self.bus.write_byte(TM1650_DISPLAY_BASE, 0)
            self.iActive = True
        except:
            self.iActive = False
        self.clear()
        self.displayOn()

    def setBrightness(self, aValue=TM1650_MAX_BRIGHT):
        if not self.iActive:
            return
        self.iBrightness = min(aValue, TM1650_MAX_BRIGHT)
        for i in range(self.iNumDigits):
            self.iCtrl[i] = (self.iCtrl[i] & TM1650_MSK_BRIGHT) | (self.iBrightness << TM1650_BRIGHT_SHIFT)
            self.bus.write_byte(TM1650_DCTRL_BASE + i, self.iCtrl[i])

    def setBrightnessGradually(self, aValue=TM1650_MAX_BRIGHT):
        if not self.iActive or aValue == self.iBrightness:
            return
        aValue = min(aValue, TM1650_MAX_BRIGHT)
        step = -1 if aValue < self.iBrightness else 1
        i = self.iBrightness
        while i != aValue:
            self.setBrightness(i)
            time.sleep(0.05)
            i += step

    def displayState(self, aState):
        if aState:
            self.displayOn()
        else:
            self.displayOff()

    def displayOn(self):
        if not self.iActive:
            return
        for i in range(self.iNumDigits):
            self.iCtrl[i] = (self.iCtrl[i] & TM1650_MSK_ONOFF) | TM1650_BIT_DOT
            self.bus.write_byte(TM1650_DCTRL_BASE + i, self.iCtrl[i])

    def displayOff(self):
        if not self.iActive:
            return
        for i in range(self.iNumDigits):
            self.iCtrl[i] = (self.iCtrl[i] & TM1650_MSK_ONOFF)
            self.bus.write_byte(TM1650_DCTRL_BASE + i, self.iCtrl[i])

    def controlPosition(self, aPos, aValue):
        if not self.iActive:
            return
        if aPos < self.iNumDigits:
            self.iCtrl[aPos] = aValue
            self.bus.write_byte(TM1650_DCTRL_BASE + aPos, aValue)

    def setPosition(self, aPos, aValue):
        if not self.iActive:
            return
        if aPos < self.iNumDigits:
            self.iBuffer[aPos] = aValue
            self.bus.write_byte(TM1650_DISPLAY_BASE + aPos, aValue)

    def setDot(self, aPos, aState):
        self.iBuffer[aPos] = self.iBuffer[aPos] & 0x7F | (0b10000000 if aState else 0)
        self.setPosition(aPos, self.iBuffer[aPos])

    def clear(self):
        if not self.iActive:
            return
        for i in range(self.iNumDigits):
            self.iBuffer[i] = 0
            self.bus.write_byte(TM1650_DISPLAY_BASE + i, 0)

    def displayString(self, aString):
        if not self.iActive:
            return
        for i in range(self.iNumDigits):
            a = ord(aString[i]) & 0b01111111
            dot = ord(aString[i]) & 0b10000000
            self.iBuffer[i] = TM1650_CDigits[a]
            if a:
                self.bus.write_byte(TM1650_DISPLAY_BASE + i, self.iBuffer[i] | dot)
            else:
                break

    def displayRunning(self, aString):
        self.iString = aString[:TM1650_MAX_STRING + 1]
        self.iPosition = self.iString
        self.displayString(self.iPosition)
        l = len(self.iPosition)
        if l <= self.iNumDigits:
            return 0
        return l - self.iNumDigits

    def displayRunningShift(self):
        if len(self.iPosition) <= self.iNumDigits:
            return 0
        self.iPosition = self.iPosition[1:]
        self.displayString(self.iPosition)
        return len(self.iPosition) - self.iNumDigits

#lds 006 class test
import sys
import serial
import time
from enum import Enum
import math

class State(Enum):
    START1 = 0
    START2 = 1
    HEADER = 2
    DATA = 3

class LDS006:
    def __init__(self, serialPort = "com10", baudRate = 115200):
        self.serialPort = serialPort
        self.baudRate = baudRate
        self.connected = False
        self.scanning = False

    def connect(self):
        if self.connected == False:
            try:
                self.ser = serial.Serial(self.serialPort, self.baudRate, timeout=0.1)
            except:
                print("Cound not connect to device")
                exit()
        self.connected = True
        self.ser.write(b'$')
        self.ser.write(b"stoplds$")
        self.scanning = False
        print("LDS Connected")

    def disconnect(self):
        self.ser.close()
        self.connected = False
        self.scanning = False

    def readBytes(self, count):
        data = self.ser.read(count)
        if len(data) != count:
                    return False
        return data

    def startLDS(self):

        if self.connected == False:
            self.connect();
        self.ser.write(b'$')
        self.ser.write(b"startlds$")
        self.scanning = True

    def stopLDS(self):
        if self.connected == False:
            return
        self.ser.write(b"stoplds$")
        self.scanning = False
        
    def getRange(self):
        if self.connected == False:
            self.connect()
        if self.scanning == False:
            self.startLDS()

        run = True
        
        angle = 0xFB
        rpm = 0
        distance = 0

        state = State.START1
        while run:
            if state == State.START1:
                data = self.readBytes(1)
                if data == False:
                    break;
                if data[0] == 0xFA:
                    state = State.DATA
                else:
                    state = State.START1
                continue
            elif state == State.DATA:
                data = self.readBytes(21)
                if data == False:
                    break
                if data[0] == 0xFB:
                    angle = 0xFB
                    rpm = 0xFB
                    return angle, rpm, distance
                angle = 4 * (data[0] - 0xA0)
                
                rpm = int(data[2] << 8) + int(data[1])

                distance += int(data[4] << 8) + int(data[3])
                #distance += int(data[8] << 8) + int(data[7])
                #distance += int(data[13] << 8) + int(data[12])
                #distance += int(data[17] << 8) + int(data[16])
                
                #distance = distance / 4
                #print("getRange " + str(angle) + " " + str(rpm/100) + " " + str(distance))
                run = False
            else:
                print("error")

        return angle, rpm, distance

if __name__ == "__main__":

    lds = LDS006()
    lds.connect()
    lds.startLDS()
    angle = 0
    while angle < 360 :
        angle,rpm,distance = lds.getRange();
        if angle != 0xFB:
            print(str(angle) + ',' + str(distance/1000))
    lds.stopLDS()

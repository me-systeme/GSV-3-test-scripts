import serial

def gsvStart():
    serialConnection.write(b'\x24')

def gsvStop():
    serialConnection.write(b'\x23')

def gsvSetZero():
    serialConnection.write(b'\x0C')

def convertMeasFrameToMeasValue(MeasFrame):
    return (float(MeasFrame[0] * 256 + MeasFrame[1])-32768)/32768


if __name__ == '__main__':
    serialConnection = serial.Serial("COM23", 38400, timeout=1)
    serialConnection.isOpen()
    gsvStart()


    for i in range(10):
        praefix = bytearray(serialConnection.read(1))[0]
        if praefix == 0xA5:
            MeasVal = bytearray(serialConnection.read(2))
            print(convertMeasFrameToMeasValue(MeasVal))

    gsvSetZero()

    try:
        while 1:
            praefix = bytearray(serialConnection.read(1))[0]
            if praefix == 0xA5:
                MeasVal = bytearray(serialConnection.read(2))
                print(convertMeasFrameToMeasValue(MeasVal))
    except:
        pass
    serialConnection.close()

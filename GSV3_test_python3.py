import serial

def gsvStart():
    serialConnection.write(b'\x24')

def gsvStop():
    serialConnection.write(b'\x23')

def gsvSetZero():
    serialConnection.write(b'\x0C')

def convertMeasFrameToMeasValue(MeasFrame):
    return ((MeasFrame[0] * 256 + MeasFrame[1])-32768)/32768


if __name__ == '__main__':
    serialConnection = serial.Serial("COM23", 38400, timeout=1)
    serialConnection.isOpen()
    gsvStart()

    for i in range(10):
        praefix = serialConnection.read(1)
        if praefix == 0xA5.to_bytes(1, byteorder='big'):
            MeasVal = serialConnection.read(2)  # .hex()
            print(convertMeasFrameToMeasValue(MeasVal))

    gsvSetZero()

    try:
        while 1:
            praefix = serialConnection.read(1)
            if praefix == 0xA5.to_bytes(1, byteorder='big'):
                MeasVal = serialConnection.read(2)  # .hex()
                print(convertMeasFrameToMeasValue(MeasVal))
    except:
        pass

    serialConnection.close()
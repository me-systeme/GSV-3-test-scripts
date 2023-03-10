import serial
from time import sleep

DATARATES = {"1_Hz":b"\x08\xb3\xb4",
			 "10_Hz":b"\x08\xf8\x5f",
			 "50_Hz":b"\x07\xfc\xf3",
			 "100_Hz":b"\x06\xfc\xf3",
			 "500_Hz":b"\x04\xfd\x8f",
			 "1000_Hz":b"\x03\xfd\x8f"}

def gsvStart():
	serialConnection.write(b'\x24')

def gsvStop():
	serialConnection.write(b'\x23')

def gsvSetZero():
	serialConnection.write(b'\x0C')

def evalDatarate(data):
	value = [k for k, v in DATARATES.items() if v == data][0]
	print(f"Datarate: {value}")

def gsvGetDatarate():
	gsvStop()
	serialConnection.reset_input_buffer()
	serialConnection.write(b'\x8B')
	data = serialConnection.read(100)
	evalDatarate(data[1:])

def gsvSetDatarate(datarate):
	key = f"{datarate}_Hz"
	value = [v for k, v in DATARATES.items() if k == key][0]
	frame = b"\x8a"+value
	serialConnection.write(frame)

def convertMeasFrameToMeasValue(MeasFrame):
	return ((MeasFrame[0] * 256 + MeasFrame[1])-32768)/32768


if __name__ == '__main__':
	serialConnection = serial.Serial("COM12", 38400, timeout=1)
	serialConnection.isOpen()
	sleep(1)
	gsvGetDatarate()
	gsvSetDatarate(10)
	sleep(0.1)
	gsvGetDatarate()

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

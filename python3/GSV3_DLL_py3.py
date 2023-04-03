import ctypes
from time import sleep

GSV_OK = 0
GSV_TRUE = 1

ComNr = ctypes.c_int(12)

def activateGSV():
	BuffSize = ctypes.c_int(1000)
	resp = dll.GSVactivate(ComNr, BuffSize)
	if resp != GSV_OK:
		print(f"Initialisierung der Baugruppe fehlgeschlagen: {resp}")

def startTransmission():
	resp = dll.GSVstartTransmit(ComNr)
	if resp != GSV_OK:
		print(f"GSVstartTransmit fehlgeschlagen: {resp}")
	sleep(1)

def stopTransmission():
	resp = dll.GSVstopTransmit(ComNr)
	if resp != GSV_OK:
		print(f"GSVstartTransmit fehlgeschlagen: {resp}")
	sleep(1)

def getSamplingRate():
	freq = ctypes.c_double(0)
	p_freq = ctypes.pointer(freq)
	factor = ctypes.c_int(0)
	p_factor = ctypes.pointer(factor)
	resp = dll.GSVreadSamplingRate(ComNr, p_freq, p_factor)
	if resp != GSV_OK:
		print(f"getSamplingRate fehlgeschlagen: {resp}")
	print(f"debug: {freq.value} {factor.value}")
	print(f"SamplingRate: {freq.value/factor.value}")
	sleep(0.1)

def setSamplingRate(freq ,factor):
	freq = ctypes.c_double(freq)
	factor = ctypes.c_int(factor)
	resp = dll.GSVwriteSamplingRate(ComNr, freq, factor)
	if resp != GSV_OK:
		print(f"setSamplingRate fehlgeschlagen: {resp}")
	sleep(0.1)

def get10MeasVals():
	out1 = ctypes.c_double(0)
	p_out1 = ctypes.pointer(out1)
	for i in range(10):
		resp = dll.GSVread(ComNr, p_out1)
		if resp != GSV_TRUE:
			print(f"resp: {resp}")
		print("Output is: " + str(out1.value))
		sleep(1/datarate)

dll = ctypes.cdll.LoadLibrary('./MEGSV.dll')
activateGSV()
stopTransmission()

getSamplingRate()
factor = 8
datarate = 1000
setSamplingRate(factor*datarate,factor)
getSamplingRate()

startTransmission()
get10MeasVals()
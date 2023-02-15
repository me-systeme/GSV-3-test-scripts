clc;clear;
pkg load instrument-control
port = serial("COM12")
pause(1)

set(port, "baudrate", 38400);
set(port, "bytesize", 8);
set(port, "parity", 'n');
set(port, "stopbits", 1);
set(port, "timeout", 1);
srl_flush(port)

for cntr=  1:100
  [rxdata, count] = srl_read(port, 3);
  recvd = char(rxdata);
  MeasVal = (((single(rxdata(2))*256) + single(rxdata(3)))-32768)/32768;
  MeasVal
  %MeasVal = MeasVal * 10
  pause(0.1);
end

fclose(port)

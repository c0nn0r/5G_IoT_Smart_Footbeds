#
# Footbed software for 5G IoT Smart Footbed
# Created by Connor Dickie 2018
#
# Modified and extended from code and libraries supplied by Adafruit Industries, including:
#
# (1)
# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
#
# (2)
# Analog Inputs for Raspberry Pi Using the MCP3008
# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain
#
#

import time
import logging
import sys
import serial

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# import IMU
from Adafruit_BNO055 import BNO055

# Create and configure the BNO sensor connection.  Make sure only ONE of the
# below 'bno = ...' lines is uncommented:
# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Added to get 10 total FSR on additional SPI channels
CLK2 = 12
MISO2 = 16
MOSI2 = 20
CS2 = 21
mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK2, cs=CS2, miso=MISO2, mosi=MOSI2)

ser = serial.Serial(port = "/dev/ttyUSB0", baudrate=115200, timeout=0)

## FOOT_ID - print FOOT_ID once.
def sensorDump():
    print('RIGHTFOOT ', end="", flush=True)
    a = 1
    # 75 is "do this for roughly 7.5 seconds"
    while a < 75:
        # read quaternion values from IMU
        x,y,z,w = bno.read_quaternion()
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        # sys, gyro, accel, mag = bno.get_calibration_status()
        # Read all the ADC channel values in a list.
        values = [0]*8
        values2 = [0]*8
        for i in range(8):
            # The read_adc function will get the value of the specified channel (0-7).
            values[i] = mcp.read_adc(i)
            values2[i] = mcp2.read_adc(i)
        # Print timestamp since unix epoch
        print("printing to serial " + str(a))
        ts = time.time()
        timestamp = str(ts)
        # Prefix the unix epoch timestamp to the sensor data to facilitate LEFT and RIGHT foot synchronization by the JumpstartCSR service.
        # Print the ADC values.
        # Print as serial bitstream in format suitable for UART
        # convert tuple to string
        tup = ('  R', timestamp, 'a{0:>3}b{1:>3}c{2:>3}d{3:>3}e{4:>3}'.format(*values), 'f{0:>3}g{1:>3}h{2:>3}i{3:>3}j{4:>3}'.format(*values2), 'x{0:0.2F}y{1:0.2F}z{2:0.2F}w{3:0.2F}'.format(x, y, z, w))
        data = ''.join(tup)
        ser.write(data.encode())
        ser.flushInput()
        ser.flushOutput()
        time.sleep(0.1)
        a = a + 1

# Talk to the Quectel LTE BG96 modem over serial UART and set the URL and port of JumpstartCSR service
def setURL():
    #ser.close()
    #ser.open()
    time.sleep(1)
    #print (ser.name)
    if ser.isOpen():
        print (ser.name)
        ser.flushInput()
        ser.flushOutput()
        ser.write(b'at\r\n')
        ser.flushInput()
        time.sleep(1)
        ser.write(b'at+qhttpurl=27,60\r\n')
        ser.flushInput()
        ser.flushOutput()
        time.sleep(1)
        ser.write(b'http://178.128.181.185:5002\r\n')
        ser.flushInput()
        ser.flushOutput()
        time.sleep(1)
        ser.write(b'at+qhttpurl?\r\n')
        ser.flushInput()
        ser.flushOutput()
        time.sleep(0.5)
        print(b">>> " + ser.readline())
    #ser.close()
    # print(response)

# Talk to the modem over serial UART and send HTTPPOST request.
def httpPost():
    time.sleep(1)
    #print (ser.name)
    if ser.isOpen():
        ser.write(b'at\r\n')
        ser.flushInput()
        ser.flushOutput()
        time.sleep(0.05)
        ser.write(b'at+qhttppost=5555\r\n')
        ser.flushInput()
        ser.flushOutput()
        time.sleep(0.7)

# ensures correct IP address and port are configured
setURL()

# Main loop
while True:
    httpPost() # initiate HTTPPOST to server
    sensorDump() # dumps for 100 count (10 seconds)
    print("waiting for 5 seconds, then sending more data.")
    time.sleep(5) # pause for 5 seconds to account for modem/network delay

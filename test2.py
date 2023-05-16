import serial
import time
import sys

"""Function that reads data from serial (through Rasp. Pi) and parses the data"""
def fetch_from_Haas():
        # Create serial object
        ser = serial.Serial(
            port = '/dev/ttyUSB0',
            baudrate = 9600,
            bytesize = serial.SEVENBITS,
            timeout = 1,
            xonxoff = True
        )
        time.sleep(1)

        while True:
            # Read Coolant Level
            try:
                ser.write(b"?Q600 1094\r\n") 
                coolant = ser.readline()
                coolant = str(float(coolant[15:26]))
                print(f"coolant is: {coolant}")
                # print(coolant)
            except Exception as a:
                coolant = '0'
                print(f"coolant is: {coolant}")
                  
        ser.close()

fetch_from_Haas()





import serial
import time
import datetime
import threading
from queue import Queue

# Variables Init
updated_values_queue = Queue()
lockData = threading.Lock()
"""Function that reads data from serial (through Rasp. Pi) and parses the data"""

def readData(ser, HAASCode):
    try:
        print("Inside readData loop...")
        ser.write(bytes("?Q600 " + HAASCode + "\r\n", "ascii"))
        print("Query ?Q600 made...")
        count = 0
        retry_limit = 10  # Limit of retries
        retries = 0       # Initial retry count

        while True:
            count += 1
            print("Inside while loop")
            value = ser.readline().decode("utf-8").strip()
            print(f"Value decoded {count} and value is [{value}]")

            if len(value) > 4:
                print("broke")
                break
            
            # Increment retries count and check if limit is reached
            retries += 1
            if retries >= retry_limit:
                print("Retry limit reached.")
                return "Unavailable"

        value = value.split(",")[2].strip()
        print(f"Value was split {count} and splitValue is [{value}]")
        value = value.replace(chr(23), '')
        print(f"Value was replaced {count} and replaceValue is [{value}]")
    except Exception as ex:
        print(ex)
        value = 'Unavailable'
    return value

#----------------------------------------------------------------------------------------#

def fetch_from_Haas():
        global combined_output, lockData, updated_values_queue

        # Create serial object (Note that these are the values configurable on Haas)
        # To ensure data collection works, the values have to be matching each other.
        ser = serial.Serial(
            # USB connection linux-based
            port = '/dev/ttyUSB0',
            # Haas Baud Rate:50/110/200/300/600/1200/2400/4800/7200/9600/19200/38400/115200
            baudrate = 115200,
            # Haas RS-232 Data Bits options: SEVENBITS or 
            bytesize = serial.SEVENBITS,
            # Haas Stop Bit options: ONE or TWO
            stopbits = serial.STOPBITS_ONE,
            # Currently set to xonxoff
            xonxoff = False,
            # Haas parity options: NONE/ZERO/EVEN/ODD
            parity = serial.PARITY_NONE,
            # Independent from Haas
            timeout = 1
        )

        # Init of values to update
        coolantPrevious = "novalue"

        while True:
            try:
                with lockData:
                # Coolant
                    coolant = readData(ser, "1094")
                    if coolant !=coolantPrevious:
                        coolantPrevious = coolant
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|coolant|" + coolant                  
                        print(f"bWork: {coolant}")
                        print(combined_output)

                    print("-----------------------------End Cycle---------------------------------")

            # Error catch
            except Exception as ex:
                print("Failed fetching values from machine: ")
                print(ex)
                time.sleep(2)

# Run the function                
fetch_from_Haas()





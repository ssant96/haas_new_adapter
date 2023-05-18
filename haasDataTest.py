import serial
import time

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
        # Create serial object
        ser = serial.Serial(
            port = '/dev/ttyUSB0',
            baudrate = 9600,
            bytesize = serial.SEVENBITS,
            timeout = 1,
            xonxoff = False
        )

        # Buffer 
        time.sleep(1)

        # Init of values to update
        xMachinePrevious = "novalue"

        while True:
            updated = False
            try:
                # Combines all output into one at the end
                outString = ""

                # X machine
                xMachine = readData(ser, "5021")
                if xMachine != xMachinePrevious:
                    outString += "|xMachine|"+xMachine
                    xMachinePrevious = xMachine
                print(f"xMachine: {xMachine}")

                print(f"--------------{outString}--------------")

            # Error catch
            except Exception as ex:
                print("Failed fetching values from machine: ")
                print(ex)
                time.sleep(2)
fetch_from_Haas()





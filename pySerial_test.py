import serial
import time

"""Function that reads data from serial (through Rasp. Pi) and parses the data"""
def fetch_from_Haas():
        # Create serial object
        ser = serial.Serial(
            port = '/dev/ttyUSB0',
            baudrate = 9600,
            bytesize = serial.SEVENBITS,
            timeout = 1,
            xonxoff = True, # Ture or False
            #parity = serial.,
            #stopbits = serial.,
            # write_timeout = ,
            # rtscts = , # True or False
            # dsrdtr = , # True or False
            # inter_byte_timeout = 
        )
        try:
            ser.open()
        except serial.SerialException:
            if ser.is_open:
                try:
                    print("Port was open. Attempting to close.")
                    ser.close()
                    time.sleep(2)
                    ser.open()
                except:
                    print("Port is already open. Failed to close. Try again.")
                    #event.clear()
            else:
                print("Failed to connect to serial port. Make sure it is free or it exists. Try again.")
                #event.clear()

        # Checks if serial port is open
        if ser.is_open(): #it might be ser.is_open:
            print("Serial port is open!")
        else:
            print("Error with serial port opening")
    
        # Data extraction from Haas
        while True:
            out = ''
            try:
                # Read Statys
                ser.write(b"Q500\r")
                status = ser.readline()
                status = status[2:-3]
                print(status)
            except:
                print("Failed to fetch values from machine")
    
    
    # Sends error message if Haas serial communication failed
    # except serial.SerialException as e:
    #     print("Failed to communicate with Haas: ", str(e))
    #     time.sleep(2)
    
    # finally:
    #     # Closes serial port
    #     if ser.is_open():
    #         ser.close()
    #         print("Serial port closed")

            ser.close()

fetch_from_Haas()
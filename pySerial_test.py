import serial
import time

"""Function that reads data from serial (through Rasp. Pi) and parses the data"""
def fetch_from_Haas():
    try:
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

        # Checks if serial port is open
        if ser.is_open(): #it might be ser.is_open:
            print("Serial port is open!")
        else:
            print("Error with serial port opening")
    
        # Data extraction from Haas
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('uft-8').strip()

                print(f"Data: {data}")

            time.sleep(1)

    # Sends error message if Haas serial communication failed
    except serial.SerialException as e:
        print("Failed to communicate with Haas: ", str(e))
    
    finally:
        # Closes serial port
        if ser.is_open():
            ser.close()
            print("Serial port closed")
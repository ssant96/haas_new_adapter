import sys
import threading
import time
import socket
import serial
import datetime

# Initialization of global attributes
client_counter = 0
client_list = []
first_run_flag = 1
combined_output = ""
lock = threading.Lock()
event = threading.Event()
event.set()

# ---------------Socket connection begins----------------#
"""Socket Objects Init"""
HOST = "0.0.0.0" #sets to any machine on the network
PORT = 7878 #default Port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

"""Binding to the local port/host"""
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print("Binding to local port/host failed. Error code: " + str(msg[0]) + " Message " + msg[1])
    sys.exit()

"""Starts Listening to Socket for Clients"""
s.listen(5)

"""Function to Clear OUT Threads List Once All Threads are Empty"""
def clear_thread_list():
    global client_list, client_counter

    while True:
        try:
            if client_counter == 0 and first_run_flag == 0 and client_list != []:
                print("%d Clients Active" % client_counter)
                # print(f"{client_counter} Clients Active") ---> more updated code
                print("Clearing All Threads....")
                for index, thread in enumerate(client_list):
                    thread.join()
                client_list = []
        except:
            print("Error with Client List Deletion")
# ---------------Socket connection ends-------------------#


# ---------------Haas Data Extraction begins--------------#
"""Function that reads data from serial (through Rasp. Pi) and parses the data"""

def readData(ser, HAASCode):
    try:
        #print("Inside readData loop...")
        ser.write(bytes("?Q600 " + HAASCode + "\r\n", "ascii"))
        #print("Query ?Q600 made...")
        count = 0
        retry_limit = 10  # Limit of retries
        retries = 0       # Initial retry count

        while True:
            count += 1
            #print("Inside while loop")
            value = ser.readline().decode("utf-8").strip()
            #print(f"Value decoded {count} and value is [{value}]")

            if len(value) > 4:
                #print("broke")
                break
            
            # Increment retries count and check if limit is reached
            retries += 1
            if retries >= retry_limit:
                print("Retry limit reached.")
                return "Unavailable"

        value = value.split(",")[2].strip()
        #print(f"Value was split {count} and splitValue is [{value}]")
        value = value.replace(chr(23), '')
        #print(f"Value was replaced {count} and replaceValue is [{value}]")
    except Exception as ex:
        print(ex)
        value = 'Unavailable'
    return value

def fetch_from_Haas():
        global combined_output
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

        # Buffer for testing purposes
        #time.sleep(1)

        # Init of values to update
        coolantPrevious = "novalue"
        spindleSpeedPrevious = "novalue"
        xMachinePrevious = "novalue"
        yMachinePrevious = "novalue"
        zMachinePrevious = "novalue"
        aMachinePrevious = "novalue"
        bMachinePrevious = "novalue"
        xWorkPrevious = "novalue"
        yWorkPrevious = "novalue"
        zWorkPrevious = "novalue"
        aWorkPrevious = "novalue"
        bWorkPrevious = "novalue"

        while True:
            try:
                # Combines all output into one at the end
                outString = ""

                # Coolant
                coolant = readData(ser, "1094")
                if coolant != coolantPrevious:
                    outString += "|coolant|"+coolant
                    coolantPrevious = coolant
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"coolant: {coolant}")
                print(f"combined output is {combined_output}")

                # Spindle Speed
                spindleSpeed = readData(ser, "3027")
                if spindleSpeed != spindleSpeedPrevious:
                    outString += "|spindleSpeed|"+spindleSpeed
                    spindleSpeedPrevious = spindleSpeed
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"spindleSpeed: {spindleSpeed}")
                print(f"combined output is {combined_output}")

                # X machine
                xMachine = readData(ser, "5021")
                if xMachine != xMachinePrevious:
                    outString += "|xMachine|"+xMachine
                    xMachinePrevious = xMachine
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"xMachine: {xMachine}")
                print(f"combined output is {combined_output}")

                # Y machine
                yMachine = readData(ser, "5022")
                if yMachine != yMachinePrevious:
                    outString += "|yMachine|"+yMachine
                    yMachinePrevious = yMachine
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"yMachine: {yMachine}")
                print(f"combined output is {combined_output}")

                # Z machine
                zMachine = readData(ser, "5023")
                if zMachine != zMachinePrevious:
                    outString += "|zMachine|"+zMachine
                    zMachinePrevious = zMachine
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"zMachine: {zMachine}")
                print(f"combined output is {combined_output}")

                # A machine
                aMachine = readData(ser, "5024")
                if aMachine != aMachinePrevious:
                    outString += "|aMachine|"+aMachine
                    aMachinePrevious = aMachine
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"aMachine: {aMachine}")
                print(f"combined output is {combined_output}")

                # B machine
                bMachine = readData(ser, "5025")
                if bMachine != bMachinePrevious:
                    outString += "|bMachine|"+bMachine
                    bMachinePrevious = bMachine
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"bMachine: {bMachine}")
                print(f"combined output is {combined_output}")

                # X work
                xWork = readData(ser, "5041")
                if xWork != xWorkPrevious:
                    outString += "|xWork|"+xWork
                    xWorkPrevious = xWork
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"xWork: {xWork}")
                print(f"combined output is {combined_output}")

                # Y work
                yWork = readData(ser, "5042")
                if yWork != yWorkPrevious:
                    outString += "|yWork|"+yWork
                    yWorkPrevious = yWork
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"yWork: {yWork}")
                print(f"combined output is {combined_output}")

                # Z work
                zWork = readData(ser, "5043")
                if zWork != zWorkPrevious:
                    outString += "|zWork|"+zWork
                    zWorkPrevious = zWork
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"zWork: {zWork}")
                print(f"combined output is {combined_output}")

                # A work
                aWork = readData(ser, "5044")
                if aWork != aWorkPrevious:
                    outString += "|aWork|"+aWork
                    aWorkPrevious = aWork
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"aWork: {aWork}")
                print(f"combined output is {combined_output}")

                # B work
                bWork = readData(ser, "5045")
                if bWork != bWorkPrevious:
                    outString += "|bWork|"+bWork
                    bWorkPrevious = bWork
                    # time stamp for more accurate readings
                    combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"bWork: {bWork}")
                print(f"combined output is {combined_output}")

                # Final data purge (Might not be needed)
                # combined_output = '\r\n' + datetime.datetime.now().isoformat() + 'Z' + outString
                # print(f"---> {combined_output}")

            # Error catch
            except Exception as ex:
                print("Failed fetching values from machine: ")
                print(ex)
                time.sleep(2)
# ---------------Haas Data Extraction ends-------------------#



# ---------------Threading Part begins-----------------------#
"""Main Thread Class For Clients"""


class NewClientThread(threading.Thread):
    # init method called on thread object creation,
    def __init__(self, conn, string_address):
        threading.Thread.__init__(self)
        self.connection_object = conn
        self.client_ip = string_address

    # run method called on .start() execution
    def run(self):
        global client_counter, combined_output
        global lock
        while True:
            try:
                # print("Sending data to Client {} in {}".format(self.client_ip, self.getName()))
                out = combined_output
                print("OUT: " + out)
                self.connection_object.sendall(out.encode())
                #time.sleep(0.5) # removed to send data faster

            except Exception as err:
                lock.acquire()
                try:
                    print(err)
                    client_counter = client_counter - 1
                    print("Connection disconnected for ip {} ".format(self.client_ip))
                    break
                finally:
                    lock.release()


"""Starts From Here"""
t1 = threading.Thread(target=clear_thread_list)
t2 = threading.Thread(target=fetch_from_Haas)
t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()
time.sleep(2)

while event.is_set():

    if first_run_flag == 1:
        print("Listening to Port: %d...." % PORT)

    try:
        conn, addr = s.accept()
        lock.acquire()
        client_counter = client_counter + 1
        first_run_flag = 0
        print("Accepting Comm From:" + " " + str(addr))
        new_Client_Thread = NewClientThread(conn, str(addr))
        new_Client_Thread.setDaemon(True)
        client_list.append(new_Client_Thread)
        print(client_list)
        new_Client_Thread.start()
        lock.release()
    except KeyboardInterrupt:
        print("\nExiting Program")
        sys.exit()

if not event.is_set():
    print("\nExiting Program")
    sys.exit()
# ----------------Threading part ends------------------------#
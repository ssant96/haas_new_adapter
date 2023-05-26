import sys
import threading
import time
import socket
import serial
import datetime
from queue import Queue

# Variables Init
client_counter = 0
client_list = []
first_run_flag = 1
combined_output = ""
updated_values_queue = Queue()
lockData = threading.Lock()
lockClient = threading.Lock()
event = threading.Event()
event.set()
data_update_event = threading.Event()

"""Socket Objects Init"""
HOST = "0.0.0.0" # sets to any machine on the network
PORT = 7878 # default Port

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
                print(f"{client_counter} Clients Active")
                print("Clearing All Threads....")
                for index, thread in enumerate(client_list):
                    thread.join()
                client_list = []
        except:
            print("Error with Client List Deletion")


"""Function that reads data from serial (through Rasp. Pi) and parses the data"""

def readData(ser, HAASCode):
    try:
        #print("Inside readData loop...")
        ser.write(bytes("?Q600 " + HAASCode + "\r\n", "ascii"))
        #print("Query ?Q600 made...")
        count = 0
        retry_limit = 10  # limit of retries
        retries = 0       # initial retry count

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

    except Exception as ex:
        print(ex)
        value = 'Unavailable'
    return value

def fetch_from_Haas():
        global combined_output, data_update_event, lockData, updated_values_queue

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
                with lockData:
                    # Coolant
                    coolant = readData(ser, "1094")
                    if coolant != coolantPrevious:
                        coolantPrevious = coolant
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|coolant|" + coolant
                        updated_values_queue.put(combined_output)
                        data_update_event.set()
                        print(f"coolant: {coolant}")

                    # Spindle Speed
                    spindleSpeed = readData(ser, "3027")
                    if spindleSpeed != spindleSpeedPrevious:
                        spindleSpeedPrevious = spindleSpeed
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|spindleSpeed|" + spindleSpeed
                        updated_values_queue.put(combined_output)
                        data_update_event.set()
                        print(f"spindleSpeed: {spindleSpeed}")

                    # X machine
                    xMachine = readData(ser, "5021")
                    if xMachine != xMachinePrevious:
                        xMachinePrevious = xMachine
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|xMachine|" + xMachine
                        updated_values_queue.put(combined_output)
                        data_update_event.set()
                        print(f"xMachine: {xMachine}")

                    # Y machine
                    yMachine = readData(ser, "5022")
                    if yMachine != yMachinePrevious:
                        yMachinePrevious = yMachine
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|yMachine|" + yMachine
                        updated_values_queue.put(combined_output)
                        data_update_event.set()
                        print(f"yMachine: {yMachine}")

                    # Z machine
                    zMachine = readData(ser, "5023")
                    if zMachine != zMachinePrevious:
                        zMachinePrevious = zMachine
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|zMachine|" + zMachine
                        updated_values_queue.put(combined_output)
                        data_update_event.set()
                        print(f"zMachine: {zMachine}")

                    # A machine
                    aMachine = readData(ser, "5024")
                    if aMachine != aMachinePrevious:
                        aMachinePrevious = aMachine
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|aMachine|" + aMachine
                        updated_values_queue.put(combined_output)
                        data_update_event.set()
                        print(f"aMachine: {aMachine}")
                    
                    # B machine
                    bMachine = readData(ser, "5025")
                    if bMachine != bMachinePrevious:
                        bMachinePrevious = bMachine
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|bMachine|" + bMachine
                        updated_values_queue.put(combined_output)
                        data_update_event.set()
                        print(f"bMachine: {bMachine}")

                    # X work
                    xWork = readData(ser, "5041")
                    if xWork != xWorkPrevious:
                        xWorkPrevious = xWork
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|xWork|" + xWork
                        updated_values_queue.put(combined_output)
                        data_update_event.set()                  
                        print(f"xWork: {xWork}") 

                    # Y work
                    yWork = readData(ser, "5042")
                    if yWork != yWorkPrevious:
                        yWorkPrevious = yWork
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|yWork|" + yWork
                        updated_values_queue.put(combined_output)
                        data_update_event.set()                    
                        print(f"yWork: {yWork}")

                    # Z work
                    zWork = readData(ser, "5043")
                    if zWork != zWorkPrevious:
                        zWorkPrevious = zWork
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|zWork|" + zWork
                        updated_values_queue.put(combined_output)
                        data_update_event.set()                     
                        print(f"zWork: {zWork}")

                    # A work
                    aWork = readData(ser, "5044")
                    if aWork != aWorkPrevious:
                        aWorkPrevious = aWork
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|aWork|" + aWork
                        updated_values_queue.put(combined_output)
                        data_update_event.set()                     
                        print(f"aWork: {aWork}")

                    # B work
                    bWork = readData(ser, "5045")
                    if bWork != bWorkPrevious:
                        bWorkPrevious = bWork
                        combined_output = '\r\n'+ datetime.datetime.now().isoformat() + 'Z' + "|bWork|" + bWork
                        updated_values_queue.put(combined_output)
                        data_update_event.set()                    
                        print(f"bWork: {bWork}")

                    print("-----------------------------End Cycle---------------------------------")

            # Error catch
            except Exception as ex:
                print("Failed fetching values from machine: ")
                print(ex)
                time.sleep(2)


"""Main Thread Class For Clients"""


class NewClientThread(threading.Thread):
    # init method called on thread object creation,
    def __init__(self, conn, string_address):
        threading.Thread.__init__(self)
        self.connection_object = conn
        self.client_ip = string_address

    # run method called on .start() execution
    def run(self):
        global client_counter, combined_output, data_update_event, lockClient, updated_values_queue
        while True:
            try:
                out = updated_values_queue.get()
                print(f"OUT: {out}")
                self.connection_object.sendall(out.encode())
                data_update_event.clear()

            except Exception as err:
                with lockClient:
                    print(err)
                    client_counter = client_counter - 1
                    print("Connection disconnected for ip {} ".format(self.client_ip))
                break


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
        print(f"Listening to Port: {PORT}....")
    try:
        conn, addr = s.accept()
        with lockClient:
            client_counter = client_counter + 1
            first_run_flag = 0
            print("Accepting Comm From:" + " " + str(addr))
            new_Client_Thread = NewClientThread(conn, str(addr))
            new_Client_Thread.setDaemon(True)
            client_list.append(new_Client_Thread)
            print(client_list)
            new_Client_Thread.start()
    except KeyboardInterrupt:
        print("\nExiting Program")
        sys.exit()

if not event.is_set():
    print("\nExiting Program")
    sys.exit()
import sys
import threading
import time
import socket
import serial
import datetime
import traceback

client_counter = 0
client_list = []
first_run_flag = 1
lock = threading.Lock()
event = threading.Event()
event.set()

# Initialization of global attributes
combined_output = ""

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
                #print("%d Clients Active" % client_counter)
                print(f"{client_counter} Clients Active") #---> more updated code
                print("Clearing All Threads....")
                for index, thread in enumerate(client_list):
                    thread.join()
                client_list = []
        except Exception as e:
            print("Error with Client List Deletion: ", e)
# ---------------Socket connection ends-------------------#


# ---------------Haas Data Extraction begins--------------#
"""Function that reads data from serial (through Rasp. Pi) and parses the data"""

def readData(ser, HAASCode):
    try:
        ser.write(bytes("?Q600 " + HAASCode + "\r\n", "ascii"))
        while True:
            value = ser.readline().decode("utf-8").strip()
            if len(value) > 4:
                break
        value = value.split(",")[2].strip()
        value = value.replace(chr(23), '')
    except Exception as ex:
        #print(ex)
        traceback.print_exc()
        value = 'Unavailable'
    return value

def fetch_from_Haas():
        global combined_output
        # Create serial object
        ser = serial.Serial(
            port = '/dev/ttyUSB0',
            baudrate = 9600,
            bytesize = serial.SEVENBITS,
            timeout = 1,
            xonxoff = False
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
            updated = False
            try:
                # Combines all output into one at the end
                outString = ""

                # Coolant
                coolant = readData(ser, "1094")
                if coolant != coolantPrevious:
                    outString += "|coolant|"+coolant
                    coolantPrevious = coolant
                print(f"coolant: {coolant}")

                # Spindle Speed
                spindleSpeed = readData(ser, "3027")
                if spindleSpeed != spindleSpeedPrevious:
                    outString += "|spindleSpeed|"+spindleSpeed
                    spindleSpeedPrevious = spindleSpeed
                print(f"spindleSpeed: {spindleSpeed}")

                # X machine
                xMachine = readData(ser, "5021")
                if xMachine != xMachinePrevious:
                    outString += "|xMachine|"+xMachine
                    xMachinePrevious = xMachine
                print(f"xMachine: {xMachine}")

                # Y machine
                yMachine = readData(ser, "5022")
                if yMachine != yMachinePrevious:
                    outString += "|yMachine|"+yMachine
                    yMachinePrevious = yMachine
                print(f"yMachine: {yMachine}")

                # Z machine
                zMachine = readData(ser, "5023")
                if zMachine != zMachinePrevious:
                    outString += "|zMachine|"+zMachine
                    zMachinePrevious = zMachine
                print(f"zMachine: {zMachine}")

                # A machine
                aMachine = readData(ser, "5024")
                if aMachine != aMachinePrevious:
                    outString += "|aMachine|"+aMachine
                    aMachinePrevious = aMachine
                print(f"aMachine: {aMachine}")

                # B machine
                bMachine = readData(ser, "5025")
                if bMachine != bMachinePrevious:
                    outString += "|bMachine|"+bMachine
                    bMachinePrevious = bMachine
                print(f"bMachine: {bMachine}")

                # X work
                xWork = readData(ser, "5041")
                if xWork != xWorkPrevious:
                    outString += "|xWork|"+xWork
                    xWorkPrevious = xWork
                print(f"xWork: {xWork}")

                # Y work
                yWork = readData(ser, "5042")
                if yWork != yWorkPrevious:
                    outString += "|yWork|"+yWork
                    yWorkPrevious = yWork
                print(f"yWork: {yWork}")

                # Z work
                zWork = readData(ser, "5043")
                if zWork != zWorkPrevious:
                    outString += "|zWork|"+zWork
                    zWorkPrevious = zWork
                print(f"zWork: {zWork}")

                # A work
                aWork = readData(ser, "5044")
                if aWork != aWorkPrevious:
                    outString += "|aWork|"+aWork
                    aWorkPrevious = aWork
                print(f"aWork: {aWork}")

                # B work
                bWork = readData(ser, "5045")
                if bWork != bWorkPrevious:
                    outString += "|bWork|"+bWork
                    bWorkPrevious = bWork
                print(f"bWork: {bWork}")

                # Final data purge
                combined_output = '\r\n' + datetime.datetime.now().isoformat() + 'Z' + outString
                print(f"------> {combined_output}")

            # Error catch
            except Exception as ex:
                print("Failed fetching values from machine: ")
                #print(ex)
                traceback.print_exc()
                time.sleep(2)

            
        ser.close()
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
                time.sleep(0.5)

            except Exception as err:
                lock.acquire()
                try:
                    #print(err)
                    traceback.print_exc()
                    client_counter = client_counter - 1
                    #print("Connection disconnected for ip {} ".format(self.client_ip))
                    print(f"Connection disconnected for ip {self.client_ip} ") #---> More updated code
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
import sys
import threading
import time
import socket
import serial
import datetime

client_counter = 0
client_list = []
first_run_flag = 1
lock = threading.Lock()
event = threading.Event()
event.set()

# ---------------Socket connection begins----=-----------#
"""Socket Objects Init"""
HOST = "0.0.0.0" #sets to any machine on the network
PORT = 7878 #default Port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

"""Binding to the local port/host"""
try:
    s.bind(HOST, PORT)
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
# ---------------Socket connection ends----==------------#


# ---------------Serial data Haas begins-===-------------#
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



# ---------------Serial data Haas ends-------------------#



# ---------------Threading part begins-------------------#
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
                print("OUT1:")
                print("OUT: " + out)
                self.connection_object.sendall(out.encode())
                time.sleep(0.5)

            except err:
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
# ---------------Threading part ends---------------------#
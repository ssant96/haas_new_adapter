import serial
import time
import datetime

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
        print(ex)
        value = 'Unavailable'
    return value


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
                print(ex)
                time.sleep(2)

            
        ser.close()

fetch_from_Haas()





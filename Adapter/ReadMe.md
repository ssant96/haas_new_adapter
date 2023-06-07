# Adapter
  
## Introduction

*Please review ReadMe.md in this project's root directory before this file for context.*

The adapter's purpose is to gather data from the targeted machine, format it and send it out to the agent through whichever port configured.

---
  
## New changes

From the changes made in the root level ReadMe.md, the following is a detailed description of each:

1. **Successfully reads data through serial port connection**: The previously mentioned Haas adapter doesn't run successfully so changes have been made to make it fully tested and working
2. **Data output to Agent method changed for better accuracy**: In the previous version, the adapter would read all data and then post a combined string with all variables and their respective new updated data which would cause the time stamps to be slightly inaccurate. In this new version, as soon as a variable is being read with a new value and it outputs it individually right away.
3. **Added thread lock to avoid data race**: because of point 2, data race issue needed to be addressed so some thread lock was implemented
4. **Added a new readData function that reads Haas serialized codes** the new readData function helps making reading data from Haas successfully and it also ensures there are retries implemented so that during Haas program changes, the code doesn't crash
5. **Improved serial connection block**: added all the possible Haas configurable variables and all their respective values that are available on the Haas.
6. **Added queue method to ensure that all data read is being sent out to the agent**: encountered an issue where new data was not being sent as fast as it was being read and therefore a queue was needed to fix this problem
7. **Better error handling**: added improved and more error handling blocks
8. **Better comments and descriptions**: Improved explanation throughout the code for better debugging

---

### How to develop the adapter

#### Data extraction 

Data extraction is most likely the hardest part of implementing an MTConnect compliant software. The following is a brief guidance:

1) What data extraction method? There are different machines out in the world. Some have built in MTConnect functionality which makes the needs for adapters negligible. Other machines have built in sensors that can output data in their own ways, and lastly there are legacy machines where sensors need to be added in order to output data. 

2) How to extract data? Once determined that machine can output data (either through built-in or added sensrs), we can begin with data extraction. Keep in mind every machine is different and some may offer USB ports, RS-232 ports, etc. and also have their own codes, software scripts, etc. In our case scenario, the Haas is able to output data through an RS-232 port that is connected to a Raspberry Pi through its USB port. Since Python was the language of choice, simply using the PySerial module to extract data from serial port is enough.

3) What data to extract? First of all, the developer needs to determine what data needs to be extracted. Some may output the entire dictionary and the adapter only needs to parse through the data of interest. For example, in a milling machine, you might want the x y z and rotational axes, machine availabilit, etc. Some other machines like the Haas for example, offer a variety of variables that can be accessed when inputting a query formatted as "Q?600 + {Haas serial code}". Please be careful with these codes and always refer to the machine specific manuals to avoid entering the wrong query which can cause damage to the machines. For Haas query codes official documentation is available [here](https://www.haascnc.com/service/troubleshooting-and-how-to/how-to/machine-data-collection---ngc.html) and the serial codes are available [here and select 13.6 System Variables](https://www.haascnc.com/service/online-operator-s-manuals/mill-operator-s-manual/mill---macros.html)

#### Data Output to Agent

Once data is extracted from the machine, the next step would be outputting it to the Agent through the Web sockets method. For future projects, the Web socket connections will most likely need to remain untouched unless changes are made in the Agent. However, keep in mind the Agent accepts data in a specific format, and as an example, lets look at how coolant is being formatted:

    # Coolant
    coolant = readData(ser, "1094")
    if coolant != coolantPrevious:
        coolantPrevious = coolant
        combined_output = '\r\n' + datetime.datetime.now().isoformat() + 'Z' + "|coolant|" + coolant 
        updated_values_queue.put(combined_output)
        data_update_event.set()
        print(f"coolant: {coolant}")

Looking at the combined_output line , the format is shown as '\r\n' + iso date time format + 'Z' + |coolant| + coolant

---

### How to run the adapter

At the Learning Factory, the adapter file is currently running in the Raspberry Pi which is connected to the Learning Factory's Wi-Fi. To run it, simply have python and PySerial installed and run 'python haasAdapter.py' or 'python3 haasAdapter.py' depending on your system. 
- If the values are being read correctly, the script should print out the values being read and the values being outputted (values followed by the "OUT:")
- If the configuration files were set up correctly, accessing localhost:5001 or whichever port specified, should show on the agent that the values were correctly received.
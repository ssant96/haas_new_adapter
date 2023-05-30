# VT Learning Factory's Haas VF-3 Adapter
  
## Introduction

*Please review ReadMe.md in this project's root directory before this file for context.*

The adapter's purpose is to gather data from the targeted machine, format it and send it out to the agent through whichever port configured.
---
  
## New changes

From the changes made in the root level ReadMe.md, the following is a detailed description of each:

1. *Successfully reads data through serial port connection*: The previously mentioned Haas adapter doesn't run successfully so changes have been made to make it fully tested and working
2. *Data output to Agent method changed for better accuracy*: In the previous version, the adapter would read all data and then post a combined string with all variables and their respective new updated data which would cause the time stamps to be slightly inaccurate. In this new version, as soon as a variable is being read with a new value and it outputs it individually right away.
3. *Added thread lock to avoid data race*: because of point 2, data race issue needed to be addressed so some thread lock was implemented
4. *Added a new readData function that reads Haas serialized codes* the new readData function helps making reading data from Haas successfully and it also ensures there are retries implemented so that during Haas program changes, the code doesn't crash
5. *Improved serial connection block*: added all the possible Haas configurable variables and all their respective values that are available on the Haas.
6. *Added queue method to ensure that all data read is being sent out to the agent*: encountered an issue where new data was not being sent as fast as it was being read and therefore a queue was needed to fix this problem
7. *Better error handling*: added improved and more error handling blocks
8. *Better comments and descriptions*: Improved explanation throughout the code for better debugging

---

### How to run the adapter

At the Learning Factory, the adapter file is currently running in the Raspberry Pi which is connected to the Learning Factory's Wi-Fi. To run it, simply have python installed and run 'python haasAdapter.py' or 'python3 haasAdapter.py' depending on your system. If the values are being read correctly, the script should print out the values being read and the values being outputted (values followed by the "OUT:")
If the configuration files were set up correctly, accessing localhost:5001 or whichever port specified, should show on the agent that the values were correctly received.
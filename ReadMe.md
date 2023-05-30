# Digitally Connected Manufacturing: A 2023 MTConnect Use Case Study at the Virginia Tech Learning Factory

## Introduction
An improved working adapter to the existing [vtech-learningfactory-haas-adapter](https://github.com/mtconnect/vtech-learningfactory-haas-adapter)

The main goal of the Learning Factory is to implement industry 4.0 across the available machines present. This project is to improve, design, test and implement a new adapter that successfully reads data from a Haas VF-3. 

In the current setup as of 2023, the Learning Factory's Haas is connected to a Raspberry Pi (linux-based) connected through USB port to the Haas (RS-232 connection) and the agent is hosted in the following custom PC:

- CPU: Intel Xeon E5-2650
- GPU: Nvidia GTX 690
- RAM: 128GB
- Storage: 1 TB
- OS: Ubuntu Linux (20.04.1 SMP)


Changes mades:
1. Successfully reads data through serial port connection
2. Data output to Agent method changed for better accuracy
3. Added thread lock to avoid data race
4. Added a new readData function that reads Haas serialized codes
5. Improved serial connection block
6. Added queue method to ensure that all data read is being sent out to the agent
7. Better error handling
8. Better comments and descriptions
---

## Browsing this Repository

The work on this project can be divided into discrete components, **each with its own folder and Readme file**:
1. The **Adapter**: contains the main adapter which is intended to be ran in the Raspberry Pi
2. **Agent Config Files** contains the xml schema for the Haas, the Learning Factory's xml schema for both the Haas and UR5, and the agent_Haas.cfg configuration file for the agent.

This project was built to comply with MTConnect version 1.8; for more information on the MTConnect standard and MTConnect Agent, please see [MTConnect's official documentation](https://www.mtconnect.org/documents).

Each component is covered in more detail in its own Readme file
---

## Installing the MTConnect Agent
**NOTE: This project used MTConnect Agent Version 1.8.0.3**

The following steps can be followed to download and install the MTConnect Agent:

1) Download MTConnect Agent from https://github.com/mtconnect/cppagent/releases?q=1.8.0.3&expanded=true
2) Extract and move ‘cppagent-1.8.0.3’ folder to Documents
3) Make a folder called ‘build’ inside ‘cppagent-1.8.0.3’ folder
4) Open terminal and cd Documents>cppagent-1.8.0.3>build and run 'cmake'
5) Run 'make'
6) Run 'sudo make install'

### How to run the adapter (Please review Adapter>ReadMe.md before attempting this part)
1) SSH into the Raspberry Pi from any device
2) Store the 'haasAdapter.py' file at a desired location
3) Run 'python haasAdapter.py' or 'python3 haasAdapter.py'

### How to start the Agent (Please review Agent Config Files>ReadMe.md before attempting this part)
1) On the device intended to run the agent, open terminal
2) cd Documents/Agent_Config_Files
3) Run 'agent run agent_Haas.cfg"

### How to view data on the Agent
1) Open any web browser on the Agent host device
2) Access http://localhost:5001
3) Alternatively, on any device on the same network, access http://{hostIPaddress:5001}
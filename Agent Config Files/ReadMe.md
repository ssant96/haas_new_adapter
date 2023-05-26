### Configuring the Agent

## Introduction

*Please review ReadMe.md in this project's root directory before this file for context.*

**Before running the agent, create a new folder called ‘Agent_Config_Files’ in the Documents folder where Haas.xml and agent_Haas.cfg will be stored.**

‘Tormach.xml’ serves the purpose of shaping the MTConnect UI to every machine, type and value that is assigned from the Adapter to the Agent. In simple words, it serves as the translator or intermediary between the Adapter and Agent.
  

‘agent.cfg’ should be configured to match the port and file path. The following is the header and it is important to specify SchemaVersion to be 1.7 so it matches the XML schema. Port was assigned to 5001 but the default is 5000.

  

	Devices = ./Haas.xml
	AllowPut = true
	ReconnectInterval = 1000
	BufferSize = 17
	SchemaVersion = 1.7
	MonitorConfigFiles = true
	Pretty = true
	Port = 5001
	MinimumConfigReloadAge = 30

  

In this part, the host is the IP address of the machine in use. This port will be important when the MTConnect web UI is being accessed from another computer in the local network.

  

	Adapters {
		#Log file has all machines with device name prefixed
		Haas-VF3
		{
			Host = 192.168.1.4
			Port = 7878
		}
	}

  

Lastly, this step is important for the agent to work. Since ‘cppagent-1.8.0.3’ folder and ‘Tormach’ folder are both in one folder (‘Documents’), the configuration should be the following:

  

	Files {
		schemas {
			Path = ../cppagent-1.8.0.3/schemas
			Location = /schemas/
		}
		styles {
			Path = ../cppagent-1.8.0.3/styles
			Location = /styles/
		}
		Favicon {
			Path = ../cppagent-1.8.0.3/styles/favicon.ico
            Location = /favicon.ico
        }
	}

---
### How to start the Agent

1) Open terminal and run Tormach_adapter.py script.
2) Open a new terminal window and cd Documents/Tormach and run 'agent run'
3) If accessing from local computer, simply run http://localhost:5001 on the web browser`
4) If accessing from another computer in the same network, run http://{insertIPaddress}:5001
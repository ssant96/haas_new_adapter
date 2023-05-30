# Agent configuration and usage

## Introduction

*Please review ReadMe.md in this project's root directory before this file for context.*

The agent serves the purpose of showcasing the data in a web UI that can be accessed once the configuration files are properly located and configured. The agent is a simple server host that will listen to socket communication and receive and display the data according to the configured schema defined in the XML schema, which in this case would be Haas.xml.

**Before running the agent, create a new folder called ‘Agent_Config_Files’ in the Documents folder where Haas.xml and agent_Haas.cfg will be stored.**

‘Haas.xml’ serves the purpose of shaping the MTConnect UI to every machine, type and value that is assigned from the Adapter to the Agent. In simple words, it serves as the translator or intermediary between the Adapter and Agent.

---

## Agent_Haas.cfg

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


In this part, the host is the IP address of the adapter's host device. Please ensure the IP address is correct as this is where the data is going to come from to the agent.

  

	Adapters {
		#Log file has all machines with device name prefixed
		Haas-VF3
		{
			Host = 192.168.1.4
			Port = 7878
		}
	}

  

Lastly, this step is important for the agent to work. Since ‘cppagent-1.8.0.3’ folder and ‘Agent Config Files’ folder are both in one folder (‘Documents’), the configuration should be the following:

  

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

To start the Agent, please follow instructions on root directory's ReadMe.md

---
## Haas.xml

The xml schema is needed to shape the UI agent access. It is important to name the variables properly and ensure it matches the MTConnect standard namings.
For more information, please refer to [MTConnect's model browser](https://model.mtconnect.org/) for how to manage each variable.
Moreover, ensure the variable names being outputted from the haasAdapter.py match the ones on the xml schema.

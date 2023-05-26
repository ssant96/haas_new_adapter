# VT Learning Factory's Haas VF-3 Adapter

  
## Introduction

*Please review ReadMe.md in this project's root directory before this file for context.*
  
## Installation and Usage Guide

These steps will provide both context on the MTConnect Agent and a guide to installing and using the Haas VF3 MTConnect Adapter. For more information on the MTConnect standard and MTConnect Agent, please see [MTConnect's official documentation](https://www.mtconnect.org/documents).

---
### Data Simulation

Under unforeseen circumstances, the Virginia Tech team was not provided with nor able to procure a functioning Tormach milling center. Instead, a data simulator was built using paper research and software investigations on a non-functioning machine. It was found that the Tormach PCNC-1100's "controller" is an instance of LinuxCNC, running on a fairly standard installation of Linux Mint. The data simulator was built around known LinuxCNC variables, with a Python dictionary schema formatted to represent as closely as possible the data that one would be able to retrieve by listening to LinuxCNC on an open port. Most variables were randomized, though positional and rotational values were smoothed from one instance to the next to add some realism.

Simulated data is accessed by this Adapter by simply importing and running the data simulator function. However, on a real machine, one would need to check the LinuxCNC configuration files and modify this Adapter to listen to the correct port, while removing the simulator import statement and adjusting the `fetch_from_Tormach` function to account for the new data source. For more context and an example of an MTConnect adapter for another LinuxCNC-based machine, refer to [the MTConnect adapter for the PocketNC milling machine](https://github.com/mtconnect/PocketNC_adapter).

---
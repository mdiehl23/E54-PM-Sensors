# E54-PM-Sensors
Dependencies:
* *pip install xlsxwriter*
* *pip install numpy*
* *sudo apt-get install matplotlib* (linux) or *pip install matplotlib* (Windows)

This is the code base for the SPS30 PM sensor. The code should be run from PMDataLogger.py.
Note that anything that was intended to be changed in the code is located and documented in the comments
of ConfigSPS30.py. PMDataLogger.py logs PM data for a specified amount of time and outputs PM10 and PM2.5 mass concentrations to a file once a second. Once this is complete, basic information about the data pull will be written to a file called *status.txt*. This code was intended for use with the E54 Spring 2021 particulate monitoring
drone senior design project. 

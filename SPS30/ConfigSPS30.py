'''
This file is in charge of holding vital information
about how the sensor will output data. Each of the variables
in this file will have a short description about how to set them.
'''

'''
This is how long the sensor will log data in seconds before
the program finishes executing
'''
TIME_SECONDS = 10

'''
This is the type of file that the program will output. This field
can be set to either "EXCEL" or "CSV"
'''
FILETYPE = 'CSV'

'''
This is a boolean value that will determine whether a graphical
output of the data will be automatically generated. When the value is
set to true, a graph will be generated. This should generally be set to false,
as the pijuice cannot display a graph. However, it will not crash the code if it
is set to true.
'''
GRAPH = False

'''
PORT must be set to the port that the sensor is using.
Ex: On windows "COM3"
Ex: On Linux "/dev/tty"....
To check your serial ports on Windows, search device manager and then go to "ports".
To check your serial ports on Linux/MacOS, type "ls /dev/tty*" into your terminal.
'''
PORT = "/dev/ttyUSB0"

'''
This is the directory that the output files will get saved to.
This will be an excel/csv and a txt output called "status.txt"
'''
DIRECTORY = '/home/pi/Desktop/'

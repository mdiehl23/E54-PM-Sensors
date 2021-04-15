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
set to true, a graph will be generated.
'''
GRAPH = True

'''
PORT must be set to the port that the sensor is using.
Ex: On windows "COM3"
Ex: On Linux "/dev/tty"....
'''
PORT = "/dev/ttyUSB0"

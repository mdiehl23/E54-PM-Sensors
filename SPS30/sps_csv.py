import sps30
import time
import numpy as np
import csv
from datetime import datetime

# Define important variables
directory = '/home/pi/Desktop/'
filename = 'PM_data.csv'
fields = ['Timestamp', 'PM2.5', 'PM10.0']
PM_Values = np.empty(shape=(0,2))

'''
Changes how long the code runs.
For example, 60 runs for 60 secs, 3600 runs for an hour
'''
TIME_SECONDS = 10

# Write fields to CSV
with open(directory+filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)

'''
This must be set to the port that the sensor is using.
Ex: On windows "COM3"
Ex: On Linux "/dev/tty"....
'''

port = "/dev/ttyUSB0"
sensor = sps30.SPS30(port)
sensor.start()

'''
The device needs to idle for a few
seconds before collecting data
'''

print("Starting data log...")
time.sleep(5)

j = 0
try:
    while(j<TIME_SECONDS):
        # Read data. This is a tuple with 10 values.
        output = sensor.read_values()
        # Format date
        now = datetime.now()
        date_str = now.strftime("%m/%d/%Y %H:%M:%S")
        # Current PM2.5 and PM10 reading
        curr_data = np.array([float(output[1]), float(output[3])])
        # Add this to the master 2D array with all the data
        PM_Values = np.insert(PM_Values,len(PM_Values),curr_data,axis=0)
        # Write values to CSV
        with open(directory+filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([date_str,PM_Values[-1][-2],PM_Values[-1][-1]])
        # Wait 1 second
        print("logging...")
        time.sleep(1)
        j+=1

    # Stop Sensor
    sensor.stop()
    sensor.close_port()
    print("Data Logging Stopped")
    
except KeyboardInterrupt:
    # Stop Sensor
    sensor.stop()
    sensor.close_port()
    print("Data Logging Stopped")

import sps30, time
import xlsxwriter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

# Make workbook
workbook = xlsxwriter.Workbook('/home/pi/Desktop/testsps30.xlsx')
worksheet = workbook.add_worksheet()

# Format columns
worksheet.write('A1', "PM2.5 (ug/m^3)")
worksheet.write('B1', "PM10.0 (ug/m^3)")

'''
This must be set to the port that the sensor is using.
Ex: On windows "COM3"
Ex: On Linux "/dev/tty"....
'''
device_port = "/dev/ttyUSB0"

sensor = sps30.SPS30(device_port)
sensor.start()

pm_25 = np.array([])
pm_10 = np.array([])
dates = []

'''
The device needs to idle for a few
seconds before collecting data
'''
print("Starting data log...")

time.sleep(5)

for i in range(2,5):
    # Read data. This is a tuple with 10 values.
    output = sensor.read_values()

    # PM2.5 is at index 1
    worksheet.write('A'+str(i), output[1])
    pm_25 = np.append(pm_25,output[1])
    # PM10 is at index 3
    worksheet.write('B'+str(i), output[3])
    pm_10 = np.append(pm_10,output[3])
    dates.append(datetime.fromtimestamp(time.time()))
    
    print("Writing to Excel...")

    time.sleep(1)

# Make Subplots
fig, (ax1,ax2) = plt.subplots(1,2)
fig.autofmt_xdate()

# PM 2.5
ax1.plot(dates,pm_25, 'tab:red')
ax1.set_title('PM 2.5 Data')
ax1.set(xlabel = 'Date', ylabel = 'ug/m^3')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M:%S'))

# PM 10
ax2.plot(dates,pm_10, 'tab:green')
ax2.set_title('PM 10 Data')
ax2.set(xlabel = 'Date', ylabel = 'ug/m^3')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M:%S'))

# Stop Sensor
sensor.stop()
sensor.close_port()

# Print Stats
print("Data logging stopped")
print("Average PM2.5 Concentration: " + str(np.average(pm_25)))
print("Average PM10 Concentration: " + str(np.average(pm_10)))

workbook.close()
plt.show()

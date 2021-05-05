#!/usr/bin/python3

import sps30, time
import xlsxwriter
import csv
import numpy as np
from datetime import datetime
import ConfigSPS30
from PMGUI import *
# only import graphing stuff if needed
if ConfigSPS30.GRAPH:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

'''
This is where the SPS30 Datalogging should be ran from.
This file reads PM data, outputs it to a file, and graphs
the data using the Sensiron SPS30 PM sensor.
@ Author: Matt Diehl
'''

# Make SPS object
try:
    sensor = sps30.SPS30(ConfigSPS30.PORT)
except:
    print("Sensor not recognized")

def formatOutput(data):
    now = datetime.now()
    date_str = now.strftime("%m/%d/%Y %H:%M:%S")
    status = open(ConfigSPS30.DIRECTORY + 'status.txt','a')
    status.write(date_str + '\n')
    status.write('Data pull successful.\n')
    status.write('Average PM 2.5: ' + str(np.average(data[:,0])) + '\n')
    status.write('Average PM 10.0: ' + str(np.average(data[:,1])) + '\n\n')
    status.close()
    
def makeGraph(x,y1,y2):
    # Make Subplots
    fig, (ax1,ax2) = plt.subplots(1,2)
    fig.autofmt_xdate()

    # PM 2.5
    ax1.plot(x,y1,'tab:red')
    ax1.set_title('PM 2.5 Data')
    ax1.set(xlabel = 'Date', ylabel = 'ug/m^3')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M:%S'))

    # PM 10
    ax2.plot(x,y2, 'tab:green')
    ax2.set_title('PM 10 Data')
    ax2.set(xlabel = 'Date', ylabel = 'ug/m^3')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M:%S'))

    plt.show(block = False)
    
def excelLog():
    PM_Values = np.empty(shape=(0,2))
    dates = []
    now = datetime.now()
    date_str = now.strftime("_%m-%d-%Y_%H%M_%Ss")
    filename = 'pm_data' + date_str + '.xlsx'

    # Make workbook
    workbook = xlsxwriter.Workbook(ConfigSPS30.DIRECTORY + filename)
    worksheet = workbook.add_worksheet()
    
    # Format columns
    worksheet.write('A1', "Timestamp")
    worksheet.write('B1', "PM2.5 (ug/m^3)")
    worksheet.write('C1', "PM10.0 (ug/m^3)")

    j = 0
    while j < ConfigSPS30.TIME_SECONDS:
        # Read data. This is a tuple with 10 values.
        output = sensor.read_values()
        # Format date
        now = datetime.now()
        date_str = now.strftime("%m/%d/%Y %H:%M:%S")
        dates.append(datetime.fromtimestamp(time.time()))
        # Current PM2.5 and PM10 reading
        curr_data = np.array([float(output[1]), float(output[3])])
        # Add this to the master 2D array with all the data
        PM_Values = np.insert(PM_Values,len(PM_Values),curr_data,axis=0)
        # Write data to workbook
        worksheet.write('A'+str(j+2), date_str)
        worksheet.write('B'+str(j+2), PM_Values[-1][-2])
        worksheet.write('C'+str(j+2), PM_Values[-1][-1])
        # Wait 1 second
        time.sleep(1)
        j+=1
        
    workbook.close()
    
    if ConfigSPS30.GRAPH:
        # This try except block ensures that we do not mix up
        # a data logging error with a graphing error
        try:
            makeGraph(dates, PM_Values[:,0],PM_Values[:,1])
        except:
            print("Failed to Graph")
            
    return PM_Values
    
def csvLog():
    PM_Values = np.empty(shape=(0,2))
    dates = []
    now = datetime.now()
    date_str = now.strftime("_%m-%d-%Y_%H%M_%Ss")
    filename = 'pm_data' + date_str + '.csv'
    fields = ['Timestamp', 'PM2.5', 'PM10.0']
    
    # Write fields to CSV
    with open(ConfigSPS30.DIRECTORY + filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

    j = 0
    while j < ConfigSPS30.TIME_SECONDS:
        # Read data. This is a tuple with 10 values.
        output = sensor.read_values()
        # Format date
        now = datetime.now()
        date_str = now.strftime("%m/%d/%Y %H:%M:%S")
        dates.append(datetime.fromtimestamp(time.time()))
        # Current PM2.5 and PM10 reading
        curr_data = np.array([float(output[1]), float(output[3])])
        # Add this to the master 2D array with all the data
        PM_Values = np.insert(PM_Values,len(PM_Values),curr_data,axis=0)
        # Write values to CSV
        with open(ConfigSPS30.DIRECTORY + filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([date_str,PM_Values[-1][-2],PM_Values[-1][-1]])
        # Wait 1 second
        time.sleep(1)
        j+=1

    if ConfigSPS30.GRAPH:
        # This try except block ensures that we do not mix up
        # a data logging error with a graphing error
        try:
            makeGraph(dates, PM_Values[:,0],PM_Values[:,1])
        except:
            print("Failed to Graph")
            
    return PM_Values

def logData():
    try:
        # Sensor needs to idle for a bit
        sensor.start()
        time.sleep(5)
        if ConfigSPS30.FILETYPE == 'EXCEL':
            data = excelLog()
            # Stop Sensor
            sensor.stop()
            sensor.close_port()
            formatOutput(data)
            # Example gui code if ever implemented
            # ss = SuccessScreen(str(np.average(data[:,0])),str(np.average(data[:,1])))
            # ss.mainloop()
            
        elif ConfigSPS30.FILETYPE == 'CSV':
            data = csvLog()
            sensor.stop()
            sensor.close_port()
            formatOutput(data)
            # Example gui code if ever implemented
            # ss = SuccessScreen(str(np.average(data[:,0])),str(np.average(data[:,1])))
            # ss.mainloop()

        # if no filetype specified, do csv
        else:
            data = csvLog()
            sensor.stop()
            sensor.close_port()
            formatOutput(data)
            
       
    except Exception as e:
        print(e)
        now = datetime.now()
        date_str = now.strftime("%m/%d/%Y %H:%M:%S")
        status = open(ConfigSPS30.DIRECTORY + 'status.txt','a')
        status.write(date_str + '\n')
        status.write('Data log failed. Reconnect sensor.\n\n')
        status.close()
        # Example gui code for failed screen
        # fs = FailedScreen()
        # fs.mainloop()

if __name__ == '__main__':
    logData()

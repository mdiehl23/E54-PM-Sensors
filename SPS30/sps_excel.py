import sps30, time
import xlsxwriter

# Make workbook
workbook = xlsxwriter.Workbook('/Users/matthewdiehl/Desktop/testsps30.xlsx')
worksheet = workbook.add_worksheet()

# Format columns
worksheet.write('A1', "PM2.5 (ug/m^3)")
worksheet.write('B1', "PM10.0 (ug/m^3)")

'''
This must be set to the port that the sensor is using.
Ex: On windows "COM3"
Ex: On Linux "/dev/tty"....
'''
device_port = "/dev/tty.usbserial-FT4R5O6P"

sensor = sps30.SPS30(device_port)
sensor.start()

# Start in column below header
i = 2

'''
The device needs to idle for a
second before collecting data
'''
time.sleep(5)

try:
    while True:
        # Read data. This is a tuple with 10 values.
        output = sensor.read_values()

        # PM2.5 is at index 1
        worksheet.write('A'+str(i), output[1])
        # PM10 is at index 3
        worksheet.write('B'+str(i), output[3])

        # Go to next cell
        i+=1
        
        '''
        Date stuff not implemented but useful
        
        date = time.localtime()
        act_date = str(date[0]) + "/" + str(date[1]) + "/" + str(date[2])
        act_time = str(date[3]) + ":" + str(date[4]) + ":" + str(date[5])

        output_data = act_date + "," + act_time + "," + sensorData[:-1] # remove comma from the end
        '''
        print("Writing to Excel...")

        time.sleep(1)

except KeyboardInterrupt:
    sensor.stop()
    sensor.close_port()
    print("Data logging stopped")
    workbook.close()

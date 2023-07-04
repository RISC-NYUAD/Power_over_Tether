import csv
from datetime import datetime
import serial
import os
import time

start = time.time()

result = [[1,2,3,4,5,6,7,8,9,10,11],[1,2,3,4,5,6,7,8,9,10,11]]
current_datetime = datetime.now()
file_name = current_datetime.strftime("DATA_%Y-%m-%d_%H-%M-%S.csv")

def read_data_from_serial():
    
    com_port = 'COM11'  # Replace with the appropriate COM port
    baud_rate = 57600  # Replace with the appropriate baud rate

    ser = serial.Serial(com_port, baud_rate)
    index=0

    try:
        numbers=[0,0,0,0,0,0,0,0,0,0,0]
        while True:
            numbers=[0,0,0,0,0,0,0,0,0,0,0]
            # Read data from the serial port
            index=index+1
            data = ser.readline().decode().strip()
            # Process the received data
            if data:
                # Split the data into a list of numbers
                data = data.split("*")
                #print(data)
                for i in range(0,10):
                    if (i==0):
                        numbers[i]=int(data[2*i], 16)*12 + int(data[2*i+1], 16) #BCM power
                    elif (i==8):
                        numbers[i]=int(data[2*i], 16)/50 + int(data[2*i+1], 16)/5000 #input current
                    elif (i==9):
                        numbers[i]=int(data[2*i], 16)*4+int(data[2*i+1], 16)/10 #input voltage
                    else:
                        numbers[i]=int(data[2*i], 16)+int(data[2*i+1], 16)/10
                #print(numbers)
                # Check if the number of values received is 10
                if len(numbers) == 11:
                    # Append the data to the Excel file
                    print(numbers)
                    #print("\n")
                    result.append(numbers)
                    #print(result)
                else:
                    print("Invalid number of values received.")

    except KeyboardInterrupt:
        end = time.time()
        with open(file_name, 'w') as file:
            writer = csv.writer(file)
            Headers=["BCM Power (W)", "BCM Current (A)", "Battery Power (kW)", "Battery Current (A)", "Bus Voltage (V)", "BCM Temperature (C)", "Efficiency (%)", "Operation Mode", "Input Current", "Input Voltage"]
            writer.writerow(Headers)
            writer.writerows(result)
            #print(index)
        ser.close()
        print("Serial connection closed.")
        print("Flight Time Duration:\n")
        print('{0:.3g}'.format(end-start)+'  Seconds or '+'{0:.3g}'.format((end-start)/60)+'  Minutes')

read_data_from_serial()

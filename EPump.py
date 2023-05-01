import csv
import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_mcp9600
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Set up GPIO to power on Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.HIGH)

# Set up I2C communication for MCP9600s
i2c = busio.I2C(board.SCL, board.SDA)
mcp1 = adafruit_mcp9600.MCP9600(i2c, address=0x67)
mcp2 = adafruit_mcp9600.MCP9600(i2c, address=0x68)

# Set up I2C communication for ADS1015s
ads1 = ADS.ADS1015(i2c, address=0x48)
ads2 = ADS.ADS1015(i2c, address=0x49)

# Set up analog inputs for ADS1015s
chan1 = AnalogIn(ads1, ADS.P0)
chan2 = AnalogIn(ads1, ADS.P1)
chan3 = AnalogIn(ads1, ADS.P2)
chan4 = AnalogIn(ads1, ADS.P3)
chan5 = AnalogIn(ads2, ADS.P0)
chan6 = AnalogIn(ads2, ADS.P1)
chan7 = AnalogIn(ads2, ADS.P2)
chan8 = AnalogIn(ads2, ADS.P3)

# Open CSV file for writing
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Write headers for data
    writer.writerow(['Time', 'Temp1 (C)', 'Temp2 (C)', 'Pressure1 (PSI)', 'Pressure2 (PSI)', 'Pressure3 (PSI)', 'Pressure4 (PSI)', 'Temp3 (C)', 'Temp4 (C)', 'Pressure5 (PSI)', 'Pressure6 (PSI)', 'Pressure7 (PSI)', 'Pressure8 (PSI)'])

    # Continuously read and store data in CSV file
    while True:
        # Get current time
        curr_time = time.time()

        # Read temperature from MCP9600s and convert to Celsius
        temp1 = mcp1.temperature - 273.15
        temp2 = mcp2.temperature - 273.15

        # Read pressure from ADS1015s and convert to PSI
        pressure1 = chan1.voltage * 100 / 4.5
        pressure2 = chan2.voltage * 100 / 4.5
        pressure3 = chan3.voltage * 100 / 4.5
        pressure4 = chan4.voltage * 100 / 4.5
        pressure5 = chan5.voltage * 100 / 4.5
        pressure6 = chan6.voltage * 100 / 4.5
        pressure7 = chan7.voltage * 100 / 4.5
        pressure8 = chan8.voltage * 100 / 4.5

        # Write data to CSV file
        writer.writerow([curr_time, temp1, temp2, pressure1, pressure2, pressure3, pressure4, temp3, temp4, pressure5, pressure6, pressure7, pressure8])

        # Wait for 1 second before reading data again
        time.sleep(1)

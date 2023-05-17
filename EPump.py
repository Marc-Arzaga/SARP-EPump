import csv
import time
import board
import busio
import adafruit_mcp9600
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO

# Define GPIO pin for triggering data collection
TRIGGER_PIN = 17

# Setup GPIO pin for input
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.IN)

# Setup I2C communication with the MCP9600 amplifiers
i2c = busio.I2C(board.SCL, board.SDA)
mcp_1 = adafruit_mcp9600.MCP9600(i2c, address=0x67)
mcp_2 = adafruit_mcp9600.MCP9600(i2c, address=0x60)

# Setup I2C communication with the ADS1015 ADCs
ads_1 = ADS.ADS1015(i2c, address=0x48)
ads_2 = ADS.ADS1015(i2c, address=0x49)

# Create analog input objects for each pressure transducer
pressure_1 = AnalogIn(ads_1, ADS.P0)
pressure_2 = AnalogIn(ads_1, ADS.P1)
pressure_3 = AnalogIn(ads_1, ADS.P2)
pressure_4 = AnalogIn(ads_1, ADS.P3)
pressure_5 = AnalogIn(ads_2, ADS.P0)
pressure_6 = AnalogIn(ads_2, ADS.P1)


# Define function for reading flow meter pulses
def read_flowmeter():
    pulse_count = 0
    while GPIO.input(TRIGGER_PIN) == GPIO.HIGH:
        pulse_count += 1
        time.sleep(0.001) # wait for 1 millisecond
    return pulse_count

# Main data collection loop
while True:
    # Wait for trigger pin to go high
    while GPIO.input(TRIGGER_PIN) == GPIO.LOW:
        pass
    
    # Read data from sensors
    temp_1 = mcp_1.temperature
    temp_2 = mcp_2.temperature
    pressure_1_psi = pressure_1.voltage * 60
    pressure_2_psi = pressure_2.voltage * 60
    pressure_3_psi = pressure_3.voltage * 60
    pressure_4_psi = pressure_4.voltage * 60
    pressure_5_psi = pressure_5.voltage * 60
    pressure_6_psi = pressure_6.voltage * 60

    pulse_count = read_flowmeter()
    
    # Write data to CSV file
    with open(f"test_run{test_run_num}.csv", "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([time.time(), temp_1, temp_2, pressure_1_psi, pressure_2_psi, pressure_3_psi, pressure_4_psi, pressure_5_psi, pressure_6_psi, pressure_7_psi, pressure_8_psi, pulse_count])
    
    # Wait for trigger pin

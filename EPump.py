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
FLOWMETER_PIN = 24

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
pressure_5 = AnalogIn(ads_2, ADS.P2)
pressure_6 = AnalogIn(ads_2, ADS.P3)

# Define boolean for startup

STARTUP = True

# Define start time

start_time = time.time()

# Define function for reading flow meter pulses
def read_flowmeter():
    pulse_count = 0
    while GPIO.input(TRIGGER_PIN) == GPIO.HIGH:
        if GPIO.INPUT(FLOWMETER_PIN) == GPIO.HIGH:
            pulse_count += 1
        time.sleep(0.001)
    return pulse_count

# Main data collection loop
while True:
    # Wait for trigger pin to go high
    while GPIO.input(TRIGGER_PIN) == GPIO.LOW:
        pass

    if (STARTUP):
        with open(f"test_run.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Time (secs)", "Temperature1", "Temperature2", "Pressure1", "Pressure2", "Pressure3", "Pressure4", "Pressure5", "Pressure6", "PulseCount"])
        STARTUP = False

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
    with open(f"test_run.csv", "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([round(time.time() - start_time, 3), round(temp_1, 3), round(temp_2, 3), round(pressure_1_psi, 3), round(pressure_2_psi, 3), round(pressure_3_psi, 3), round(pressure_4_psi, 3), round(pressure_5_psi, 3), round(pressure_6_psi, 3), pulse_count])

    # Wait for trigger pin

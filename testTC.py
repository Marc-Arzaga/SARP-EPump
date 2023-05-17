import csv
import time
import os
import board
import busio
import adafruit_mcp9600

# Thermocouple configurations
thermocouple1 = adafruit_mcp9600.MCP9600(busio.I2C(board.SCL, board.SDA), address=0x67)
thermocouple2 = adafruit_mcp9600.MCP9600(busio.I2C(board.SCL, board.SDA), address=0x66)

# CSV file path
csv_file = os.path.join(os.path.expanduser("~"), "Desktop", "thermocouple_data.csv")

# Create CSV file if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "Temperature 1 (C)", "Temperature 2 (C)"])

# Data collection loop
start_time = time.time()
collecting_data = False

while True:
    # Check if data collection should start or stop
    user_input = input("Enter 'start' to begin data collection or 'stop' to finish: ")

    if user_input.lower() == "start":
        if not collecting_data:
            collecting_data = True
            start_time = time.time()
            print("Data collection started.")
    elif user_input.lower() == "stop":
        if collecting_data:
            collecting_data = False
            print("Data collection stopped.")
            break
    else:
        print("Invalid input. Enter 'start' or 'stop'.")

    # Read and log temperature data
    if collecting_data:
        current_time = time.time() - start_time
        temperature1 = thermocouple1.temperature
        temperature2 = thermocouple2.temperature

        with open(csv_file, mode="a") as file:
            writer = csv.writer(file)
            writer.writerow([current_time, temperature1, temperature2])

        print(f"Time: {current_time:.2f}s, Temperature 1: {temperature1:.2f}°C, Temperature 2: {temperature2:.2f}°C")

    # Delay between data samples
    time.sleep(0.5)

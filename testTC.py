import csv
import time
import board
import busio
import adafruit_mcp9600

# Initialize I2C bus and MCP9600 objects
i2c = busio.I2C(board.SCL, board.SDA)
mcp9600_1 = adafruit_mcp9600.MCP9600(i2c, address=0x67)
mcp9600_2 = adafruit_mcp9600.MCP9600(i2c, address=0x60)

# Create and open the CSV file for writing
csv_file_path = "/home/pi/Desktop/thermocouple_data.csv"
csv_file = open(csv_file_path, mode="w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp", "Temperature 1", "Temperature 2"])

try:
    while True:
        # Read temperatures from both MCP9600s
        temperature_1 = mcp9600_1.temperature
        temperature_2 = mcp9600_2.temperature

        # Get the current timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Write data to the CSV file
        csv_writer.writerow([timestamp, temperature_1, temperature_2])
        csv_file.flush()  # Flush the buffer to ensure data is written immediately

        # Wait for 1 second before the next reading
        time.sleep(1)

except KeyboardInterrupt:
    # Close the CSV file and clean up
    csv_file.close()

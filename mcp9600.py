import time
import board
import busio
import adafruit_mcp9600

# Initialize I2C bus and MCP9600 sensor
i2c = busio.I2C(board.SCL, board.SDA)
mcp = adafruit_mcp9600.MCP9600(i2c)

# Main loop
while True:
    # Read temperature data from MCP9600 sensor
    temp = mcp.temperature

    # Display temperature data on laptop via Ethernet connection
    with open('/dev/tcp/{laptop_ip_address}/{port_number}', 'w') as sock:
        sock.write(f"Temperature: {temp:.2f} °C\n")

    # Wait for a second before taking the next reading
    time.sleep(1)

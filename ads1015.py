import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import socket

# Initialize I2C bus and ADS1015 ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)

# Configure ADC channels
channels = [AnalogIn(ads, ADS.P0),
            AnalogIn(ads, ADS.P1),
            AnalogIn(ads, ADS.P2),
            AnalogIn(ads, ADS.P3)]

# Initialize Ethernet socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 12345))  # Replace 12345 with the desired port number
s.listen(1)

# Wait for connection from laptop
print('Waiting for connection from laptop...')
conn, addr = s.accept()
print('Connected by', addr)

# Read ADC and send data over Ethernet
while True:
    # Read ADC values and encode as string
    data = ''
    for channel in channels:
        data += str(channel.value) + ','
    data = data[:-1] + '\n'  # Remove last comma and add newline character
    
    # Print ADC values to console
    print('ADC values:', data.strip())
    
    # Send data over Ethernet to laptop
    conn.sendall(data.encode('utf-8'))
    
    # Wait for acknowledgement from laptop
    try:
        conn.recv(1024)
    except socket.error:
        print('Connection closed by laptop')
        break
    
    # Wait before reading again to avoid overwhelming laptop with data
    time.sleep(0.1)

# Close connection and ADC
conn.close()
ads.deinit()

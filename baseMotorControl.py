import pigpio # Import the pigpio library to control the Raspberry Pi's GPIO pins
import socket # Import the socket library to establish newtork connections

ESC_PIN = 18 # The GPIO pin that is connected to the ESC PWM wire
pi = pigpio.pi() # Creating a new instance of the pigpio library
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a new TCP/IP socket for network communcation
server_address = ('', 10000)  # Change to the IP address of your Raspberry Pi if required
sock.bind(server_address)
sock.listen(1) # Listen for incoming connections
conn, addr = sock.accept() # Wait for a new client to connect

current_speed = 0 # Initial motor speed
MAX_SPEED = 30000 # Set maximum motor RPM to 30,000
SPEED_INCREMENT = 500 # Set speed increment to 500 RPM

# Function to set motor speed
def set_speed(speed):
    pi.set_servo_pulsewidth(ESC_PIN, speed)

while True:
    try:
        # receive data from the client
        data = conn.recv(1024).decode()
        
        # Check the data recieved and adjust motor speed accordingly
        if data == "left": # Decrease motor speed in increments
            current_speed -= SPEED_INCREMENT
            if current_speed < 0:
                current_speed = 0
            set_speed(current_speed)
        elif data == "right": # Increase motor speed in increments
            current_speed += SPEED_INCREMENT 
            if current_speed > MAX_SPEED:
                current_speed = MAX_SPEED
            set_speed(current_speed)
        elif data == "up": # Set motor speed to max speed
            current_speed = MAX_SPEED
            set_speed(current_speed)
        elif data == "down": # Stop motor
            current_speed = 0
            set_speed(current_speed)
    except KeyboardInterrupt:
        # clean up on Ctrl-C
        set_speed(0)
        pi.stop()
        conn.close()
        sock.close()
        break

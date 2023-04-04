import RPi.GPIO as GPIO
import time

# Setup GPIO pin for ESC signal
ESC_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_PIN, GPIO.OUT)

# Set initial PWM value
PWM_FREQ = 50
ESC_PWM = GPIO.PWM(ESC_PIN, PWM_FREQ)
ESC_PWM.start(0)

# Set speed control parameters
MIN_RPM = 0
MAX_RPM = 10000
STEP_RPM = 100

# Function to convert RPM to PWM duty cycle
def rpm_to_duty_cycle(rpm):
    return (rpm - MIN_RPM) / (MAX_RPM - MIN_RPM) * 100

# Wait for keyboard input
while True:
    char = input("Press 'u' for Up arrow key, 'd' for Down arrow key, or 'q' to quit: ")
    if char == 'u' or char == 'U':  # Up arrow key
        new_rpm = min(int(ESC_PWM.duty_cycle) + STEP_RPM, MAX_RPM)
        ESC_PWM.ChangeDutyCycle(rpm_to_duty_cycle(new_rpm))
    elif char == 'd' or char == 'D':  # Down arrow key
        new_rpm = max(int(ESC_PWM.duty_cycle) - STEP_RPM, MIN_RPM)
        ESC_PWM.ChangeDutyCycle(rpm_to_duty_cycle(new_rpm))
    elif char == 'q' or char == 'Q':  # Quit
        break

# Clean up GPIO pins
ESC_PWM.stop()
GPIO.cleanup()

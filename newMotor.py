import RPi.GPIO as GPIO
import time
import getch

# Setup GPIO pin for ESC signal
ESC_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_PIN, GPIO.OUT)

# Set initial PWM value
PWM_FREQ = 50
ESC_PWM = GPIO.PWM(ESC_PIN, PWM_FREQ)
ESC_PWM.start(0)

# Set speed control parameters
MIN_PWM = 5
MAX_PWM = 10
STEP_PWM = 1

# Wait for keyboard input
while True:
    char = getch.getch()
    if char == '\x1b[A':  # Up arrow key
        ESC_PWM.ChangeDutyCycle(min(ESC_PWM.duty_cycle + STEP_PWM, MAX_PWM) )
    elif char == '\x1b[B':  # Down arrow key
        ESC_PWM.ChangeDutyCycle(max(ESC_PWM.duty_cycle - STEP_PWM, MIN_PWM) )
    elif char == '\x03':  # Ctrl+C
        break

# Clean up GPIO pins
ESC_PWM.stop()
GPIO.cleanup()

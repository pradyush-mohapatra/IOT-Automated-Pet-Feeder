import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from time import sleep

# Define MQTT broker details (replace with your actual values)
broker_address = "io.adafruit.com"
username = "own username"
password = "own password"

# Define servo pin (replace with your actual pin number)
servo_pin = 11

# Function to set servo position based on duty cycle
def set_servo_position(duty_cycle):
    servo.ChangeDutyCycle(duty_cycle)  # Set PWM duty cycle

# Function to handle incoming MQTT messages
def on_message(client, userdata, msg):
    if msg.topic == "username/feeds/pet_feed" and msg.payload.decode() == "feed":
        print("Received message: Feed pet!")
        # Set servo to dispense food position (adjust duty cycle as needed)
        set_servo_position(7)  # Duty cycle for 90 degrees (food dispensing)
        sleep(1)  # Adjust dispense duration as needed
        # Set servo back to neutral position
        set_servo_position(2)  # Duty cycle for 0 degrees (neutral)

# Connect to MQTT broker
client = mqtt.Client()
client.username_pw_set(username, password)
client.on_message = on_message
client.connect(broker_address)

# Start MQTT subscription
client.subscribe("user name/feeds/pet_feed")
client.loop_start()

try:
    # Set GPIO numbering mode (replace with BCM if needed)
    GPIO.setmode(GPIO.BOARD)

    # Set servo pin as output
    GPIO.setup(servo_pin, GPIO.OUT)

    # Initialize PWM for servo control (adjust frequency as needed)
    servo = GPIO.PWM(servo_pin, 50)  # 50Hz pulse frequency

    # Start PWM with initial duty cycle (neutral position)
    servo.start(2)  # Duty cycle for 0 degrees (neutral)

    print("Pet feeder ready. Waiting for MQTT messages...")

    # Keep the program running indefinitely (or implement a termination mechanism)
    while True:
        pass

except KeyboardInterrupt:
    # Clean up on exit (stop PWM, reset GPIO pins)
    servo.stop()
    GPIO.cleanup()
    
    print("Exiting program...")

client.loop_stop()
client.disconnect()

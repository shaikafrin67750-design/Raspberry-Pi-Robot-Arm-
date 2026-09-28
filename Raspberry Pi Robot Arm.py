import RPi.GPIO as GPIO
import time

# GPIO pins for servo motors
BASE = 17
SHOULDER = 18
ELBOW = 27
GRIPPER = 22

# GPIO setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(BASE, GPIO.OUT)
GPIO.setup(SHOULDER, GPIO.OUT)
GPIO.setup(ELBOW, GPIO.OUT)
GPIO.setup(GRIPPER, GPIO.OUT)

# Create PWM signals
base_servo = GPIO.PWM(BASE, 50)
shoulder_servo = GPIO.PWM(SHOULDER, 50)
elbow_servo = GPIO.PWM(ELBOW, 50)
gripper_servo = GPIO.PWM(GRIPPER, 50)

base_servo.start(0)
shoulder_servo.start(0)
elbow_servo.start(0)
gripper_servo.start(0)


# Convert angle to PWM duty cycle
def set_angle(servo, angle):
    duty = 2.5 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)


# Move robot arm to home position
def home_position():
    print("Moving to home position...")

    set_angle(base_servo, 90)
    set_angle(shoulder_servo, 90)
    set_angle(elbow_servo, 90)
    set_angle(gripper_servo, 30)


# Pick object
def pick_object():
    print("Picking object...")

    # Move arm down
    set_angle(shoulder_servo, 120)
    set_angle(elbow_servo, 60)

    # Open gripper
    set_angle(gripper_servo, 20)

    time.sleep(1)

    # Close gripper
    set_angle(gripper_servo, 70)

    # Lift arm
    set_angle(shoulder_servo, 80)
    set_angle(elbow_servo, 90)


# Place object
def place_object():
    print("Placing object...")

    # Rotate base
    set_angle(base_servo, 150)

    # Move arm down
    set_angle(shoulder_servo, 120)
    set_angle(elbow_servo, 60)

    # Open gripper
    set_angle(gripper_servo, 20)

    time.sleep(1)

    # Return arm
    set_angle(shoulder_servo, 90)
    set_angle(elbow_servo, 90)
    set_angle(base_servo, 90)


# Main program
try:
    print("Raspberry Pi Robot Arm")

    home_position()

    time.sleep(2)

    pick_object()

    time.sleep(2)

    place_object()

    print("Operation completed.")

except KeyboardInterrupt:
    print("Program stopped.")

finally:
    base_servo.stop()
    shoulder_servo.stop()
    elbow_servo.stop()
    gripper_servo.stop()

    GPIO.cleanup()

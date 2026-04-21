import utime

from machine import Pin, PWM
from time import sleep

# SERVOS

#rotates a servo n times between 0°, 90° and 180°
def rotate_cardinally(pin, cycles):
    # Set up PWM Pin for servo control
    servo_pin = Pin(pin)
    servo = PWM(servo_pin)

    # Set Duty Cycle for Different Angles

    # i recommend precalculating  the angles
    # to avoid repetitive processing !!!
    
    max_duty = 7864
    min_duty = 1802
    half_duty = min_duty + int((max_duty-min_duty)/2) # half point between min and max


    #Set PWM frequency
    frequency = 50
    servo.freq (frequency)

    for i in range(0, cycles):
        #Servo at 0 degrees
        servo.duty_u16(min_duty)
        print("spun servo to 0° \n")
        sleep(1)
    
        #Servo at 90 degrees
        servo.duty_u16(half_duty)
        print("spun servo to 90° \n")
        sleep(1)
    
        #Servo at 180 degrees
        servo.duty_u16(max_duty)
        print("spun servo to 180° \n")
        sleep(1)

        #Servo at 90 degrees
        servo.duty_u16(half_duty)
        print("spun servo to 90° \n")
        sleep(1)

        print(f"end of cycle {i} :)\n\n\n")
        sleep(1)


# CLOCK 
def millis():
    start = utime.ticks_ms()

    while True:
        if utime.ticks_diff(utime.ticks_ms(), start) > 1000:
            print("1 sec")
            start_time = utime.ticks_ms()

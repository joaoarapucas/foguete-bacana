from servo import Servo
from barometer import Barometer
from csv_logger import CSVLogger
from timer import current_ms, elapsed_ms

from picozero import pico_led
import utime

pico_led.on()

# --------------- CONSTS --------------- #
MEASURE_INTERVAL_MS = 500
SERVO_TRIGGER_HEIGHT = 0.75 # (m)
SERVO_ACTIVE_ANGLE = 45


# --------------- MODULES SETUP --------------- #
servo = Servo(pin=28)
print("check: servo ok!")

baro = Barometer(sda_pin=0, scl_pin=1)
print("check: barometer ok!")

p0 = baro.calibrate_p0(samples=10)
print(f"check: P0 = {p0:.2f} hPa")


# --------------- I/O SETUP --------------- #
csv_io = CSVLogger(["Time (ms)", "Temperature (°C)", "Pressure (hPa)", "Height (m)"])
print(f"check: logging to {csv_io.filename}")


# --------------- MAIN --------------- #
start_time = current_ms()
last_measure_ms = start_time
print("check: timer started!\n")

while True:
    now = current_ms()
    delta_t = utime.ticks_diff(now, last_measure_ms)

    if delta_t >= MEASURE_INTERVAL_MS:
        last_measure_ms = now

        data = baro.read()
        
        time = elapsed_ms(start_time)
        temp = data['t']
        press = data['p']
        height = data['h']

        csv_io.append([f"{time}",
                       f"{temp:.4f}",
                       f"{press:.4f}",
                       f"{height:.4f}"])

        print(f"TEMPERATURE: {temp:.1f}°C")
        print(f"PRESSURE:    {press:.3f} hPa")
        print(f"TIME:        {time} ms")
        print(f"HEIGHT:      {height:.2f} m\n")
        
        servo.rotate_to(SERVO_ACTIVE_ANGLE if height >= SERVO_TRIGGER_HEIGHT else 0)
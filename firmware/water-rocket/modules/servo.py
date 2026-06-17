from machine import Pin, PWM
import utime

class Servo:
    """
    simplifies the use of a servo motor
    (tested using a SG90)
    """
    
    # --------------- CONSTANTS --------------- #
    MIN_DUTY = 1802
    MAX_DUTY = 7864
    FREQUENCY = 50

    def __init__(self, pin: int):
        self._pwm = PWM(Pin(pin))
        self._pwm.freq(self.FREQUENCY)

    # --------------- PUBLIC METHODS --------------- #

    def rotate_to(self, degrees: float) -> None:
        """rotates the servo to a specific angle (0–180°)"""
        self._pwm.duty_u16(self._degrees_to_duty(degrees))

    def rotate_cardinally(self, cycles: int = 1) -> None:
        """
        rotates between 0°, 90° and 180° for n cycles;
        useful for testing and debugging.
        """
        positions = [
            (0,   self.MIN_DUTY),
            (90,  self._degrees_to_duty(90)),
            (180, self.MAX_DUTY),
            (90,  self._degrees_to_duty(90)),
        ]

        for i in range(cycles):
            for angle, duty in positions:
                self._pwm.duty_u16(duty)
                print(f"spun servo to {angle}°")
                utime.sleep(1)
            print(f"end of cycle {i}\n")

    def off(self) -> None:
        """disables the PWM signal (servo holds position but stops receiving signal)."""
        self._pwm.deinit()

    # --------------- PRIVATE HELPERS --------------- #

    def _degrees_to_duty(self, degrees: float) -> int:
        """
        since to actually set the servo angle we must use
        duty cycles instead of degrees, this function
        makes the code clearer to read by accepting degrees
        """
        degrees = max(0.0, min(180.0, degrees))
        proportion = degrees / 180.0
        delta_duty = self.MAX_DUTY - self.MIN_DUTY
        
        return self.MIN_DUTY + int(proportion * delta_duty)
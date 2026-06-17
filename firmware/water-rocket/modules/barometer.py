from bmp280 import BMP280I2C
from machine import I2C, Pin

class Barometer:
    """
    simplifies the use of the BMP 280
    by automatically doing most of the calculations
    
    notes:
        -it requires I2C0 pins
        -to calculate P0 it uses the avg. of readings
         at the start of the program instead of using
         actual sea level values from weather stations
    """

    def __init__(self, sda_pin: int = 0, scl_pin: int = 1,
                 i2c_id: int = 0, address: int = 0x76, freq: int = 400_000
                 ):

        i2c = I2C(i2c_id,
                  sda=Pin(sda_pin),
                  scl=Pin(scl_pin),
                  freq=freq)

        self._sensor = BMP280I2C(address, i2c)
        self._p0: float | None = None

    # --------------- PUBLIC METHODS --------------- #

    def calibrate_p0(self, samples: int = 10) -> float:
        """
        calculates avg. readings at start to set it
        as reference for height calculations later
        """
        total = sum(self._sensor.measurements['p'] for _ in range(samples))
        self._p0 = total / samples
        return self._p0

    def read(self) -> dict:
        """
        returns a dict with keys:
          't' – temperature (°C)
          'p' – pressure (hPa)
          'h' – height (m) (requires calibrated p0)
        """
        m = self._sensor.measurements
        return {
            't': m['t'],
            'p': m['p'],
            'h': self.calc_height(m['p']),
        }

    def calc_height(self, hpa: float, p0: float | None = None) -> float:
        """
        calculates the height using an adapted
        and simplified barometric formula
        """
    
        reference = p0 if p0 is not None else self._p0
        if reference is None:
            raise ValueError("P0 not set — call calibrate_p0() first.")

        return 44330.0 * (1.0 - (hpa / reference) ** (1.0 / 5.255))

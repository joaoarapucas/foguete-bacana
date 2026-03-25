import utime

def millis():
    start = utime.ticks_ms()

    while True:
        if utime.ticks_diff(utime.ticks_ms(), start) > 1000:
            print("1 sec")
            start_time = utime.ticks_ms()

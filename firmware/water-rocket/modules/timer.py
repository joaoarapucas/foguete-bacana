import utime

def current_ms() -> int:
    """returns the current time in (ms)"""
    return utime.ticks_ms()

def elapsed_ms(start: int) -> int:
    """returns milliseconds elapsed since start"""
    return utime.ticks_diff(utime.ticks_ms(), start)
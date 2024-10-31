import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)

class GroveWS2813RgbStrip(PixelStrip):
    def __init__(self, pin, count, brightness=None):
        if brightness is None:
            brightness = LED_BRIGHTNESS

        # Create PixelStrip object with appropriate configuration.
        super(GroveWS2813RgbStrip, self).__init__(
            count,
            pin,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            brightness
        )

        # Initialize the library (must be called once before other functions).
        self.begin()

def flash(strip, color, num_flashes=3, flash_duration=0.5):
    """Flash all LEDs three times."""
    for _ in range(num_flashes):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(flash_duration)

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()
    time.sleep(flash_duration)

def colorWipe(strip, color, wait_ms=100, acceleration=1.2, max_speed_km_h=20):
    """Wipe color across the LED strip with a group of three LEDs at a time, with acceleration."""
    strip_length_m = 10  # 1 meter
    led_distance_m = strip_length_m / strip.numPixels()

    speed_km_h = 0.1  # initialize to a small non-zero value
    acceleration_factor = acceleration

    for i in range(strip.numPixels() - 2):
        strip.setPixelColor(i, color)
        strip.setPixelColor(i + 1, color)
        strip.setPixelColor(i + 2, color)
        strip.show()

        delay_time = led_distance_m / (speed_km_h / 3.6)
        acceleration_factor = 1 + (acceleration - 1) * (1 - speed_km_h / max_speed_km_h) ** 2
        speed_km_h *= acceleration_factor

        if speed_km_h > max_speed_km_h:
            speed_km_h = max_speed_km_h
            acceleration_factor = 1  # stop accelerating once max speed is reached

        print(f"Speed: {speed_km_h:.2f} km/h")

        time.sleep(delay_time)

        strip.setPixelColor(i, 0)
        strip.setPixelColor(i + 1, 0)
        strip.setPixelColor(i + 2, 0)

def main():
    import sys
    count = 200
    pin = 18 # Default pin
    
    if len(sys.argv) >= 2:
        pin = int(sys.argv[1])
    if len(sys.argv) >= 3:
        count = int(sys.argv[2])

    strip = GroveWS2813RgbStrip(pin, count)

    print('Press Ctrl-C to quit.')
    try:
        while True:
            print('Color wipe and flash animations.')
            flash(strip, Color(0, 100, 0))  # Green flash
            colorWipe(strip, Color(0, 100, 0))  # Green wipe
    except KeyboardInterrupt:
        # Clear all LEDs when exit
        colorWipe(strip, Color(0, 0, 0), 10)

if __name__ == '__main__':
    main()

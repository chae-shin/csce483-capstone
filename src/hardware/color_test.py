from rpi_ws281x import PixelStrip, Color
import time

# LED strip configuration:
LED_COUNT      = 450     # Total number of LEDs (8 groups * 50 LEDs per group)
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800kHz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # Set to 0 for GPIOs 18, 19, 41, 45 or 53

def main():
    # Initialize the LED strip
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    # Define the colors (as (R, G, B) tuples)
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 200, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 100, 0),  # Orange
        (102, 0, 204),  # Purple
        # (255, 255, 255)
    ]

    # Ensure we have exactly 8 colors
    if len(colors) != 9:
        print("Error: Exactly 8 colors are required.")
        return

    leds_per_group = 50  # Each group has 50 LEDs

    # Set colors for each group
    for group in range(7, 9):
        start_led = group * leds_per_group
        end_led = start_led + leds_per_group
        color = colors[group]
        r, g, b = color

        for i in range(start_led, end_led):
            strip.setPixelColor(i, Color(r, g, b))

    # Update the LEDs
    strip.show()

    # Keep the colors displayed for a certain duration (e.g., 10 seconds)
    time.sleep(10)

    # Clear the strip at the end
    clear_strip(strip)

def clear_strip(strip):
    """Turn off all the LEDs."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

if __name__ == "__main__":
    main()

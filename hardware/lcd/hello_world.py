import i2c_def as I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()

# mylcd.lcd_display_string("Hello World", 1)
# mylcd.lcd_display_string("Raspberry Pi", 2)
myString = "Hello World! My name is Bruh lol."

# Scroll the text left to right
while True:
    for i in range (0, len(myString)):
        mylcd.lcd_display_string(myString[i:(i+16)], 1)
        sleep(0.8)
       

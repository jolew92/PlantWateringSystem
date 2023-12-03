from machine import ADC, Pin, I2C
import utime
from pico_i2c_lcd import I2cLcd
 
# use variables instead of numbers:
soil = ADC(Pin(28)) # Connect Soil moisture sensor data to Raspberry pi pico GP28
 
#Calibraton values
min_moisture=25000
max_moisture=65535

redLED = Pin(3,Pin.OUT)
greenLED = Pin(2,Pin.OUT)
greenflag = 1

# LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000) # object to communicate with the LCD screen over the I2C protocol
I2C_ADDR = i2c.scan()[0] # this will store the first I2C address found when we scan the bus
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16) # object to set up the I2C connection from the libery 
 
lcd.hide_cursor()
 
while True:
    moisture = (max_moisture-soil.read_u16())*100/(max_moisture-min_moisture) 
    if moisture > 100:
        moisture = 100
    print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
    utime.sleep(0.1) 
    
    if soil.read_u16() > 40000:
        greenLED.value(0)
        lcd.clear()
        lcd.putstr("Uwaga! " + "%.2f" % moisture +"%\n")
        lcd.putstr("Potrzebuje wody!\n")
        print(str(soil.read_u16()))
        
        for i in range(5):
            redLED.value(1)
            utime.sleep(0.2)
            redLED.value(0)
    else:
        greenLED.value(1)
        lcd.clear()
        lcd.putstr("Nie potrzebuje\n")
        lcd.putstr("wody :) " + "%.2f" % moisture +"%\n")
        print(str(soil.read_u16()))
        utime.sleep(0.5)
        greenLED.value(0)
        utime.sleep(0.3)
    utime.sleep(0.1)
        
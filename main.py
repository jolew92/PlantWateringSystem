from machine import ADC, Pin
import utime
 
# use variables instead of numbers:
soil = ADC(Pin(28)) # Connect Soil moisture sensor data to Raspberry pi pico GP28
 
#Calibraton values
min_moisture=18644
max_moisture=65535

redLED = Pin(3,Pin.OUT)
greenLED = Pin(2,Pin.OUT)
greenflag = 1
 
#greenLED.value(1)
 
while True:
    moisture = (max_moisture-soil.read_u16())*100/(max_moisture-min_moisture) 
    print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")
    utime.sleep(0.1) 
    
    if soil.read_u16() > 40000:
        greenLED.value(0)
        print("Need water!")
        print(str(soil.read_u16()))
        for i in range(5):
            redLED.value(1)
            utime.sleep(0.1)
            redLED.value(0)
    else:
        greenLED.value(1)
        print("I don't need water")
        print(str(soil.read_u16()))
        utime.sleep(0.5)
        greenLED.value(0)
        utime.sleep(0.3)
    utime.sleep(0.1)
        
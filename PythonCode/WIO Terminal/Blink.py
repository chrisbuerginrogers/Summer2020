#https://github.com/Seeed-Studio/Seeed_Ardupy_Sketchbook


from machine import Pin, Map
import time

LED = Pin(Map.LED_BUILTIN, Pin.OUT)

while True:
    LED.on()
    time.sleep(1)
    LED.off()
    time.sleep(1)
    
    
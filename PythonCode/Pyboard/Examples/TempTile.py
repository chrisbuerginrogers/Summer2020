'''
https://pybd.io/hw/tile_sensa.html

two different i2c addresses, 64 and 69 for temp and light
LEDs on X2,3,4
'''

class HDC2080:
     def __init__(self, i2c, addr=64):
          self.i2c = i2c
          self.addr = addr

     def is_ready(self):
          return self.i2c.readfrom_mem(self.addr, 0x0f, 1)[0] & 1 == 0

     def measure(self):
          self.i2c.writeto_mem(self.addr, 0x0f, b'\x01')

     def temperature(self):
          data = self.i2c.readfrom_mem(self.addr, 0x00, 2)
          data = data[0] | data[1] << 8
          return data / 0x10000 * 165 - 40

     def humidity(self):
          data = self.i2c.readfrom_mem(self.addr, 0x02, 2)
          data = data[0] | data[1] << 8
          return data / 0x10000 * 100
          
class OPT3001:
     def __init__(self, i2c, addr=69):
          self.i2c = i2c
          self.addr = addr

     def is_ready(self):
          return bool(self.i2c.readfrom_mem(self.addr, 0x01, 2)[1] & 0x80)

     def measure(self):
          self.i2c.writeto_mem(self.addr, 0x01, b'\xca\x10')

     def lux(self):
          data = self.i2c.readfrom_mem(self.addr, 0, 2)
          return 0.01 * 2 ** (data[0] >> 4) * ((data[0] & 0x0f) << 8 | data[1])


from machine import Pin, Signal
import utime
import machine, SystemLink

i2c = machine.I2C('X')
hdc = HDC2080(i2c)
opt = OPT3001(i2c)
led_b = Signal('X4', Pin.OUT, value=0, invert=True)

fred2 = SystemLink.SystemLink('fred2','STRING')
fred2.connect()

while True:
     hdc.measure()
     opt.measure()
     led_b.on()
     while not hdc.is_ready():
          machine.idle()
     print(hdc.temperature(), hdc.humidity())
     while not opt.is_ready():
          machine.idle()
     print(opt.lux())
     if fred2.status():
          fred2.put(str(hdc.temperature()))
     led_b.off()
     utime.sleep(1)

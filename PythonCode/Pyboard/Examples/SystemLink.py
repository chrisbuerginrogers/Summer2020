'''
This talks to SystemLink 

fred2 = SystemLink('fred2','STRING')
fred2.connect()
fred2.status()
fred2.get()
a,b = fred2.put('test')
if b == 'Tag Value Updated':
     print('success')
     
'''
import machine, network, ubinascii, ujson, urequests, utime
     
class SystemLink(object):
     def __init__(self,tag,type = 'STRING'):
          self.WiFi = network.WLAN()
          mac = ubinascii.hexlify(network.WLAN().config("mac"),":").decode()
          print("MAC address: " + mac)
          self.SSID = 'username'
          self.passwd = 'password'
          self.Key = "key"
          self.tag = tag
          self.type = type
          self.url_tag = "https://api.systemlinkcloud.com/nitag/v2/tags/" + tag
          self.url_value = self.url_tag + '/values/current'
          self.headers = {"Accept":"application/json","x-ni-api-key":self.Key}

     def connect(self):
          status = True
          if not self.WiFi.isconnected():
               print ("Connecting ..")
               self.WiFi.active(True)
               self.WiFi.connect(self.SSID,self.passwd)
               i=0
               while i < 25 and not self.WiFi.isconnected():
                    utime.sleep_ms(200)
                    i=i+1
               if self.WiFi.isconnected():
                    print ("Connection succeeded")
               else:
                    print ("Connection failed")
                    status = False
          return status
                    
     def status(self):
          return self.WiFi.isconnected()
                    
     def put(self,value):
          propName={"type":self.type,"path":self.tag}
          propValue = {"value":{"type":self.type,"value":value}}

          try:
               setTag = urequests.put(self.url_tag,headers=self.headers,json=propName).text
               setValue = urequests.put(self.url_value,headers=self.headers,json=propValue).text
          except:
               setTag = 'error'
               setValue = 'error'
          return setTag,setValue

     def get(self):
          try:
               value = urequests.get(self.url_value,headers=self.headers).text
               data = ujson.loads(value)
               result = data.get("value").get("value")
               print ("value = ",result)
          except:
               result = 'error'
          return result
          

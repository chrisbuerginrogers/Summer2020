import requests
import passwords as p

#BasePath = '/Users/crogers/Desktop/'
BasePath = '/home/pi/Documents/PythonCode/HouseCode/images/'

def SL_setup():
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     Key = p.Keys['SystemLink']
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     return urlBase, headers
     
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlTag = urlBase + Tag
     urlValue = urlBase + Tag + "/values/current"
     propName={"type":Type,"path":Tag}
     propValue = {"value":{"type":Type,"value":Value}}
     #try:
     #     requests.put(urlTag,headers=headers,json=propName,timeout=1).text
     #except Exception as e:
     #    print('SL define error: ' + e)
     try:
          requests.put(urlValue,headers=headers,json=propValue,timeout=1).text
     except Exception as e:
          print('SL put error: ' + str(e))
     return 

def Get_SL(Tag):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = urequests.get(urlValue,headers=headers,timeout=1).text
          data = ujson.loads(value)
          result = data.get("value").get("value")
     except Exeption as e:
          print('SL GET error: ' + str(e))
     return result

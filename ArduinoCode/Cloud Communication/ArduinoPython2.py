from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

oauth_client = BackendApplicationClient(client_id="ZjF8grzu418SRhSBqfKot4tjQ7xSH9iz")
token_url = "https://api2.arduino.cc/iot/v1/clients/token"

oauth = OAuth2Session(client=oauth_client)
token = oauth.fetch_token(
    token_url=token_url,
    client_id="ZjF8grzu418SRhSBqfKot4tjQ7xSH9iz",
    client_secret="QeZD94Bif2vCO0hYYNxoOCdT6kURs5ZxJFXb40eFlNecuLMIWD0d7oX6DcQW2kBO",
    include_client_id=True,
    audience="https://api2.arduino.cc/iot",
)

print(token.get("access_token"))

import iot_api_client as iot
from iot_api_client.rest import ApiException
from iot_api_client.configuration import Configuration

# configure and instance the API client
client_config = Configuration(host="https://api2.arduino.cc/iot")
client_config.access_token = token.get("access_token")
client = iot.ApiClient(client_config)

# as an example, interact with the devices API
devices_api = iot.DevicesV2Api(client)

try:
    resp = devices_api.devices_v2_list()
    print(resp)
except ApiException as e:
    print("Got an exception: {}".format(e))

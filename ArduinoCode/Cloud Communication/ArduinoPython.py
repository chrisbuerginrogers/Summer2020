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

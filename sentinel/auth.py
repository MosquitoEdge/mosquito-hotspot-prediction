from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from login import client_id, client_secret

# Create a session
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

# Get token for the session
token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/oauth/token',
                          client_id=client_id, client_secret=client_secret)

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

url = "https://services.sentinel-hub.com/api/v1/statistics"

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from clouds import gen_clouds
from auth import client, oauth, token

# Cloud cover V
# Temperature
# Humidity
# Soil moisture
# Precipitation

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

url = "https://services.sentinel-hub.com/api/v1/statistics"


def main():
    response = oauth.request("POST", url=url, headers=headers, json=gen_clouds(
        (
            3238005, 5039853, 3244050, 5045897
        )
    ))

    sh_statistics = response.json()

    print(sh_statistics)


main()

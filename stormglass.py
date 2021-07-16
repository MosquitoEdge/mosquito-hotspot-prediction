import arrow
from typing import Dict, Tuple
import requests

API_KEY = "d32ee2b4-e57a-11eb-80ed-0242ac130002-d32ee32c-e57a-11eb-80ed-0242ac130002"

def weather(point: Tuple[float], start: str, end: str) -> Dict:
    return requests.get(
        "https://api.stormglass.io/v2/weather/point",
        params={
            "lat": point[0],
            "lng": point[1],
            # This many params will consume a huge number of your available reuests:
            # "params": ','.join(["cloudCover", "airTemperature", "humidity", "precipitation", "pressure", "iceCover"]),
            # So when testing, try with a single param to see the data format, etc:
            "params": "cloudCover",
            "start": start,
            "end": end,
        },
        headers={"Authorization": API_KEY},
    )


def bio(point: Tuple[float], start: str, end: str) -> Dict:
    return requests.get(
        "https://api.stormglass.io/v2/bio/point",
        params={
            "lat": point[0],
            "lng": point[1],
            "params": "soilMoisture",
            "start": start,
            "end": end,
        },
        headers={"Authorization": API_KEY},
    )


def main():
    point = (58.7984, 17.8081)
    start = arrow.get("2018-05-15")

    print(
        weather(
            point, start.to("UTC").timestamp(), start.shift(days=1).to("UTC").timestamp()
        ).json()
    )


main()

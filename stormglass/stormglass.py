import arrow
import pandas as pd
from typing import Dict, Tuple
import requests

API_KEY = "2eb05852-e5d5-11eb-9f40-0242ac130002-2eb058ca-e5d5-11eb-9f40-0242ac130002"


def weather(point: Tuple[float], start: str, end: str) -> Dict:
    return requests.get(
        "https://api.stormglass.io/v2/weather/point",
        params={
            "lat": point[0],
            "lng": point[1],
            # This many params will consume a huge number of your available reuests:
            "params": ",".join(
                [
                    "cloudCover",
                    "airTemperature",
                    "humidity",
                    "precipitation",
                    "pressure",
                    "iceCover",
                ]
            ),
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
    neon = pd.read_csv(
        "C:\\Users\\gnana\\Documents\\Code\\mosquito-hotspot-prediction\\stormglass\\neon.csv"
    )

    for _, row in neon.iterrows():
        latitude = float(row["Latitude"])
        longitude = float(row["Longitude"])
        date = arrow.get(row["Date"])

        data = weather(
            (latitude, longitude),
            date.to("UTC").timestamp(),
            date.shift(minutes=1).to("UTC").timestamp(),
        ).json()
        print(data)

        values = data["hours"][0] if len(data["hours"]) != 0 else None
        if values is not None:
            temp = (
                values["airTemperature"]["noaa"]
                if "airTemperature" in values.keys()
                else None
            )
            humidity = values["humidity"]["noaa"] if "humidity" in values.keys() else None
            pressure = values["pressure"]["noaa"] if "pressure" in values.keys() else None
            precipitation = (
                values["precipitation"]["noaa"]
                if "precipitation" in values.keys()
                else None
            )
        
            cloudCover = (
                values["cloudCover"]["noaa"] if "cloudCover" in values.keys() else None
            )
        else:
            temp =  None
            humidity =  None
            pressure =  None
            precipitation = None
            cloudCover = None

        # print(
        #     f"temp={temp}, humidity={humidity}, pressure={pressure}, precipitation={precipitation}, cloudCover={cloudCover}"
        # )


if __name__ == "__main__":
    main()

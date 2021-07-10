from datetime import datetime
from typing import Dict, Tuple
from auth import oauth, url, headers

now = datetime.now().isoformat(timespec='seconds') + "Z"


def gen_temp(bbox: Tuple[float], from_date: str = "2021-04-01T00:00:00Z", to_date: str = now) -> Dict:
    evalscript = """
            //VERSION=3
            function setup() {
            return {
                input: [{
                bands: [
                    "CLM",
                    "dataMask"
                ]
                }],
                output: [
                {
                    id: "data",
                    bands: 1
                },
                {
                    id: "dataMask",
                    bands: 1
                }]
            }
            }
            function evaluatePixel(samples) {
                return {
                    data: [samples.CLM],
                    dataMask: [samples.dataMask]
                }
            }
            """
    return {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/EPSG/0/3857"
                }
            },
            "data": [
                {
                    "type": "sentinel-3-slstr",
                    "dataFilter": {
                        "mosaickingOrder": "leastRecent"
                    }
                }
            ]
        },
        "aggregation": {
            "timeRange": {
                "from": from_date,
                "to": to_date
            },
            "aggregationInterval": {
                "of": "P1D"
            },
            "evalscript": evalscript,
            "resx": 10,
            "resy": 10
        },
    }


def temperature_fetch(bbox: Tuple[float]) -> Dict:
    response = oauth.request(
        "POST", url=url, headers=headers, json=gen_temp(bbox))
    stats = response.json()
    return stats

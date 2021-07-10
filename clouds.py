from datetime import datetime
from typing import Dict, Tuple


now = datetime.now().isoformat(timespec='seconds') + "Z"

# Percentage of cloudy pixels for selected area of interest (default is EPSG:3857)


def gen_clouds(bbox: Tuple[float], from_date: str = "2021-04-01T00:00:00Z", to_date: str = now) -> Dict:
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
                    "type": "sentinel-2-l2a",
                    # "type": "sentinel-3-slstr",
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

from datetime import datetime
from typing import Dict, Tuple
from auth import oauth, url, headers

now = datetime.now().isoformat(timespec="seconds") + "Z"


def gen_water(
    bbox: Tuple[float], from_date: str = "2021-04-01T00:00:00Z", to_date: str = now
) -> Dict:
    evalscript = """
                //VERSION=3
                function setup() {
                    return {
                        input: [{
                        bands: [
                            "B09",
                            "dataMask"
                        ]
                        }],
                        output: [
                        {
                            id: "output_B09",
                            bands: 1,
                            sampleType: "FLOAT32"
                        },
                        {
                            id: "dataMask",
                            bands: 1
                        }]
                    }
                }
                function evaluatePixel(samples) {
                    return {
                        output_B09: [samples.B09],
                        dataMask: [samples.dataMask]
                    }
                }
                """

    return {
        "input": {
            "bounds": {
                "bbox": bbox,
                "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/3857"},
            },
            "data": [
                {
                    "type": "sentinel-2-l2a",
                    "dataFilter": {"mosaickingOrder": "leastRecent"},
                }
            ],
        },
        "aggregation": {
            "timeRange": {"from": from_date, "to": to_date},
            "aggregationInterval": {"of": "P1D"},
            "evalscript": evalscript,
            "resx": 10,
            "resy": 10,
        },
        "calculations": {
            "default": {
                "histograms": {
                    "default": {"nBins": 5, "lowEdge": 0.0, "highEdge": 0.3}
                },
                "statistics": {"default": {"percentiles": {"k": [33, 50, 75, 90]}}},
            }
        },
    }


def water_fetch(
    bbox: Tuple[float], from_date: str = "2021-04-01T00:00:00Z", to_date: str = now
) -> Dict:
    response = oauth.request(
        "POST", url=url, headers=headers, json=gen_water(bbox, from_date, to_date)
    )
    stats = response.json()
    return stats

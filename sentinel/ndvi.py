from datetime import datetime
from typing import Dict, Tuple
from auth import oauth, url, headers

now = datetime.now().isoformat(timespec="seconds") + "Z"


def gen_ndvi(
    bbox: Tuple[float], from_date: str = "2021-04-01T00:00:00Z", to_date: str = now
) -> Dict:
    evalscript = """
                //VERSION=3
                function setup() {
                    return {
                        input: [{
                        bands: [
                            "B04",
                            "B08",
                            "SCL",
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
                    let ndvi = (samples.B08 - samples.B04)/(samples.B08 + samples.B04)
                    
                    var validNDVIMask = 1
                    if (samples.B08 + samples.B04 == 0 ){
                        validNDVIMask = 0
                    }
                    
                    var noWaterMask = 1
                    if (samples.SCL == 6 ){
                        noWaterMask = 0
                    }

                    return {
                        data: [ndvi],
                        // Exclude nodata pixels, pixels where ndvi is not defined and water pixels from statistics:
                        dataMask: [samples.dataMask * validNDVIMask * noWaterMask]
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
                {"type": "sentinel-2-l2a", "dataFilter": {"mosaickingOrder": "leastCC"}}
            ],
        },
        "aggregation": {
            "timeRange": {"from": "2020-01-01T00:00:00Z", "to": "2020-12-31T00:00:00Z"},
            "aggregationInterval": {"of": "P30D"},
            "evalscript": evalscript,
            "resx": 10,
            "resy": 10,
        },
    }


def ndvi_fetch(
    bbox: Tuple[float], from_date: str = "2021-04-01T00:00:00Z", to_date: str = now
) -> Dict:
    response = oauth.request(
        "POST", url=url, headers=headers, json=gen_ndvi(bbox, from_date, to_date)
    )
    stats = response.json()
    return stats

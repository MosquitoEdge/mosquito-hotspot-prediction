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
      bands: ["S7", "S8", "S9", "F1", "F2"] 
    }],
    output: {
      bands: 5,
      sampleType: "UINT16"
    }
  }
}

function multiplyband(sample){
  // Multiply by 100
  return 100 * sample;
}

function evaluatePixel(sample) {
  // Return the bands multiplied by 100 as integers to save processing units. 
  // To obtain reflectance or BT values, simply divide the resulting pixel values by 100.
  return [multiplyband(sample.S7), multiplyband(sample.S8), multiplyband(sample.S9), 
          multiplyband(sample.F1), multiplyband(sample.F2)]
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
                    },
                    "orbitDirection": "DESCENDING"
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
            "resx": 500,
            "resy": 500
        },
    }


def temperature_fetch(bbox: Tuple[float]) -> Dict:
    response = oauth.request(
        "POST", url=url, headers=headers, json=gen_temp(bbox))
    stats = response.json()
    return stats

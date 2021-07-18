import json
import datetime as dt
from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sentinelhub import SentinelHubStatistical, DataCollection, CRS, BBox, bbox_to_dimensions, \
    Geometry, SHConfig, parse_time, parse_time_interval, SentinelHubStatisticalDownloadClient

from sentinelhub import SHConfig

from sentinelhub import SHConfig
import arrow
from openpyxl import Workbook

config = SHConfig()

config.sh_client_id = 'd84ec113-bfc8-4c67-a075-5eb344a278df'
config.sh_client_secret = 'Qba7.>E^o0mtPm5D}JT[(xRrsQvtQp27Eq5MAMtZ'
config.save()

neon = pd.read_csv("2var_mosquitoFINAL.csv")

wb = Workbook()
wb['Sheet'].title = "api"
sh1 = wb.active

for _, row in neon.iterrows():
    longitude = float(row["Longitude"])
    latitude = float(row["Latitude"])
    #print(longitude)
    #print(latitude)
    date = arrow.get(row["Date"])
    #print (date.strftime("%Y-%m-%d"))
    #print (date.shift(days=-5).to("UTC").strftime("%Y-%m-%d"))
    betsiboka_bbox = BBox([longitude-0.5, latitude-0.5, longitude+0.5, latitude+0.5], CRS.WGS84)

    rgb_evalscript = """
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

    rgb_request = SentinelHubStatistical(
        aggregation=SentinelHubStatistical.aggregation(
            evalscript=rgb_evalscript,
            time_interval=(date.shift(days=-5).to("UTC").strftime("%Y-%m-%d"), date.strftime("%Y-%m-%d")),
            aggregation_interval='P1D',
            size=(631, 1047)
        ),
        input_data=[
            SentinelHubStatistical.input_data(
                DataCollection.SENTINEL2_L2A,
                maxcc=0.8
            )
        ],
        bbox=betsiboka_bbox,
        config=config
    )


    rgb_stats = rgb_request.get_data()[0]

    #print(rgb_stats)
    try:
        mean = rgb_stats['data'][0]['outputs']['output_B09']['bands']['B0']['stats']['mean']
        print(mean)
        sh1.append([latitude, longitude, mean])
        wb.save("watervapor6.xlsx")
    except:
        print ("Hi")
        sh1.append([latitude, longitude, None])
        wb.save("watervapor6.xlsx")

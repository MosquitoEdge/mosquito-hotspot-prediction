import arrow
import pandas as pd
from typing import Dict, Tuple
import requests
from openpyxl import Workbook
import time
import warnings
import random

warnings.filterwarnings("ignore")
wb = Workbook()
wb['Sheet'].title = "ArcGIS"
sh1 = wb.active


while True:
    count=0
    tempbool=True
    humiditybool=True
    pressurebool=True
    precipitationbool=True
    cloudCoverbool=True

    temp=None
    humidity=None
    pressure=None
    precipitation=None
    cloudCover=None

    def getStormGlass (longitude, latitude, date):
        API_KEY = "2eb05852-e5d5-11eb-9f40-0242ac130002-2eb058ca-e5d5-11eb-9f40-0242ac130002"
        arr=[]
        #date=arrow.get (date)
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

        def main():
            global count
            global temp
            global humidity
            global pressure
            global precipitation
            global cloudCover

            data = weather(
                (latitude, longitude),
                date.to("UTC").timestamp(),
                date.shift(minutes=1).to("UTC").timestamp(),
            ).json()
            # print(data)

            values = data["hours"][0] if len(data["hours"]) != 0 else None
            if values is not None:

                #Temperature
                try:
                    temp = (
                        values["airTemperature"]["noaa"]
                        if "airTemperature" in values.keys()
                        else None
                    )
                except:
                    try:
                        temp = (
                            values["airTemperature"]["dwd"]
                            if "airTemperature" in values.keys()
                            else None
                        )
                    except:
                        try:
                            temp = (
                                values["airTemperature"]["smhi"]
                                if "airTemperature" in values.keys()
                                else None
                            )
                        except:
                            temp=None

                #Humidity

                try:
                    humidity = (
                        values["humidity"]["noaa"]
                        if "humidity" in values.keys()
                        else None
                    )
                except:
                    try:
                        humidity = (
                            values["humidity"]["dwd"]
                            if "humidity" in values.keys()
                            else None
                        )
                    except:
                        try:
                            humidity = (
                                values["humidity"]["smhi"]
                                if "humidity" in values.keys()
                                else None
                            )
                        except:
                            humidity=None

                #Pressure
                try:
                    pressure = (
                        values["pressure"]["noaa"]
                        if "pressure" in values.keys()
                        else None
                    )
                except:
                    try:
                        pressure = (
                            values["pressure"]["dwd"]
                            if "pressure" in values.keys()
                            else None
                        )
                    except:
                        try:
                            pressure = (
                                values["pressure"]["smhi"]
                                if "pressure" in values.keys()
                                else None
                            )
                        except:
                            pressure=None


                #Precipitation
                try:
                    precipitation = (
                        values["precipitation"]["noaa"]
                        if "precipitation" in values.keys()
                        else None
                    )
                except:
                    try:
                        precipitation = (
                            values["precipitation"]["dwd"]
                            if "precipitation" in values.keys()
                            else None
                        )
                    except:
                        try:
                            precipitation = (
                                values["precipitation"]["smhi"]
                                if "precipitation" in values.keys()
                                else None
                            )
                        except:
                            precipitation=None

                #CloudCover
                try:
                    cloudCover = (
                        values["cloudCover"]["noaa"]
                        if "cloudCover" in values.keys()
                        else None
                    )
                except:
                    try:
                        cloudCover = (
                            values["cloudCover"]["dwd"]
                            if "cloudCover" in values.keys()
                            else None
                        )
                    except:
                        try:
                            cloudCover = (
                                values["cloudCover"]["smhi"]
                                if "cloudCover" in values.keys()
                                else None
                            )
                        except:
                            cloudCover=None

            else:
                temp = None
                humidity = None
                pressure = None
                precipitation = None
                cloudCover = None
                print ("no data for this input")

            global tempbool
            global humiditybool
            global pressurebool
            global precipitationbool
            global cloudCoverbool
            #arr.append (longitude) #Change
            #arr.append (latitude) #Change
            if temp is None:
                count += 1
                tempbool=False
            else:
                arr.append(float(temp))
            if humidity is None:
                count+=1
                humiditybool=False
            else:
                arr.append(float(humidity))
            if pressure is None:
                count+=1
                pressurebool=False
            else:
                arr.append(float(pressure))
            if precipitation is None:
                count+=1
                precipitationbool=False
            else:
                arr.append(float(precipitation))
            if cloudCover is None:
                count+=1
                cloudCoverbool=False
            else:
                arr.append(float(cloudCover))

        main()

        return arr
    def RandomForests (array):
        from sqlalchemy import create_engine
        import pymysql
        import pandas as pd

        dataset = pd.read_csv("C:/Users/aviba/PycharmProjects/colors/ClimateVars (cleaned).csv")

        #for x, row in dataset.iterrows():
            #dataset ['Presence'].iloc [x]=int (dataset ['Presence'].iloc [x])
            #print (type (dataset ['Presence'].iloc [x]))
        #2019-12-11T13:05Z

        #print (dataset.iloc [0]['Presence'])
        #print (type (print (dataset ['Presence'])))
        #print (pd.unique(dataset ['Presence']))
        #print(dataset.head())

        counter=5-count #Change
        #print ("Number of vars: "+str (counter))

        #if lon==False: #Change
            #dataset = dataset.drop('Longitude', 1)
            #print("lon")
        #if lat==False: #Change
            #dataset = dataset.drop('Latitude', 1)
            #print("lat")
        if tempbool==False:
            dataset = dataset.drop('Temperature', 1)
            #print ("temp")
        if humiditybool==False:
            dataset = dataset.drop('Humidity', 1)
            #print ("hum")
        if pressurebool==False:
            dataset = dataset.drop('Pressure', 1)
            #print ("press")
        if precipitationbool==False:
            dataset = dataset.drop('Precipitation', 1)
            #print ("precip")
        if cloudCoverbool==False:
            dataset = dataset.drop('Cloud Cover', 1)
            #print ("cloud")

        #print (dataset)

        X = dataset.iloc[:, 0: counter].values
        y = dataset.iloc [:, counter].values


        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
        # print(X_train)

        from sklearn.ensemble import RandomForestClassifier

        classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
        classifier.fit(X_train, y_train)

        if counter == 1:
            pred = [[array[0]]]
        if counter == 2:
            pred = [[array[0], array[1]]]
        if counter == 3:
            pred = [[array[0], array[1], array[2]]]
        if counter == 4:
            pred = [[array[0], array[1], array[2], array[3]]]
        if counter == 5:
            pred = [[array[0], array[1], array[2], array[3], array[4]]]
        #if counter == 6:
            #pred = [[array[0], array[1], array[2], array[3], array[4], array [5]]]
        #if counter == 7:
            #pred = [[array[0], array[1], array[2], array[3], array[4], array[5], array[6]]]

        finalpred = classifier.predict(pred)
        thepred = classifier.predict_proba(pred)

        #print(finalpred)
        #print(thepred)

        y_pred = classifier.predict(X_test)

        #from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

        #print(confusion_matrix(y_test, y_pred))
        #print(classification_report(y_test, y_pred))
        #print(accuracy_score(y_test, y_pred))

        #from matplotlib import pyplot

        #importance = classifier.feature_importances_

        #for i, v in enumerate(importance):
            #print('Feature: %0d, Score: %.5f' % (i, v))

        #pyplot.bar([x for x in range(len(importance))], importance)
        #pyplot.show()

        newarr = thepred[0]
        return float (newarr [1])

    longitude=random.randint(-66,124) #Change this
    latitude=random.randint(26,49) #Change this

    date=arrow.get("2021-07-21T13:05Z")

    arr=getStormGlass(longitude, latitude, date)

    if tempbool==False and humiditybool==False and pressurebool==False and precipitationbool==False and cloudCoverbool==False:
        sh1.append ([longitude, latitude, None])
        wb.save("ArcGISDashboard9.xlsx")
    else:
        val=RandomForests(arr)
        print (val)
        sh1.append([longitude, latitude, temp, humidity, pressure, precipitation, cloudCover, val])
        wb.save("ArcGISDashboard9.xlsx")


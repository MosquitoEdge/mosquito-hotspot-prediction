from clouds import cloud_fetch
from water import water_fetch
from temperature import temperature_fetch
from ndvi import ndvi_fetch

# Cloud cover
# Temperature
# Humidity
# Soil moisture
# Precipitation

# bbox = (3.741855, 40.6300454, 3.7267418, 40.6363157)
bbox = (414315.00, 4958219.00, 414858.98, 4958819.00)

def main():
    # print(cloud_fetch(bbox))
    # print(water_fetch(bbox))
    print(ndvi_fetch(bbox))
    # print(temperature_fetch(bbox))

main()


from water import water_fetch
from clouds import cloud_fetch
from temperature import temperature_fetch

# Cloud cover
# Temperature
# Humidity
# Soil moisture
# Precipitation

# 4326
bbox = (3.721855, 40.6320454, 3.7267418, 40.6361357)
# 3857
# bbox = (414315.00, 4958219.00, 414858.98, 4958819.00)

def main():
    print(cloud_fetch(bbox))
    print(water_fetch(bbox))
    # print(temperature_fetch(bbox))


main()

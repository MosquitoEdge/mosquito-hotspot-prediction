from clouds import cloud_fetch
from temperature import temperature_fetch

# Cloud cover
# Temperature
# Humidity
# Soil moisture
# Precipitation

bbox = (3238005, 5039853, 3244050, 5045897)


def main():
    # print(cloud_fetch(bbox))
    print(temperature_fetch(bbox))


main()

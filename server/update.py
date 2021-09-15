#!/usr/bin/env python3

template = """
  const ${name} = { lat: ${lat}, lng: ${lng} };
  const marker_${name} = new google.maps.Marker({
    position: ${name},
    map: map,
  });
}
"""

def main():
    name,lat,lng = "uluru",-25.344,131.036
    filledin = template.replace("${name}", name).replace("${lat}", str(lat)).replace("${lng}", str(lng))
    with open("index.js", "a") as f:
        f.write(filledin)

main()

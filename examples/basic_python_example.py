import json
import math

import requests

def main():

    src = [{"name": "ESO013-G012",
            "RAJ2000": 0.29250263822381634 * (180./math.pi),
            "DECJ2000": -1.4016351371821572 * (180./math.pi)}]
    print(src)
    lon, lat, el = 54.368591, 24.482149, 0.0

    url = "https://ephem-api.herokuapp.com/get_ephem"
    headers = {"content-type":"application/json"}
    r = requests.post(url,data=json.dumps(
         {"observer_details":{"lon":lon, "lat":lat, "el":el},
          "sources":src}
    ), headers=headers)

    print(r.json())


if __name__ == '__main__':
    main()

import os
import json
import logging
import math
import unittest

import numpy as np

from src.api import EphemAPI

cur_dir = os.path.dirname(os.path.abspath(__name__))

class TestAPI(unittest.TestCase):

    sample_data_json = os.path.join(cur_dir, "sample_data/sources.json")

    @classmethod
    def setUpClass(self):
        with open(self.sample_data_json, "r") as f:
            srcs = json.load(f)
        srcs_list = []
        for key in srcs:
            src = {"name":key,
                   "RAJ2000":srcs[key]['ra'] * (180./math.pi),
                   "DECJ2000":srcs[key]['dec'] * (180./math.pi)}
            srcs_list.append(src)
        self.srcs = srcs_list
        self.api = EphemAPI()

    def test_get_ephem(self):
        logger = logging.getLogger("TestAPI.test_get_ephem")
        n_srcs, atol = 50, 1e-3
        lon, lat, el = -211.019942862, -35.403983527 , 688.867
        observer_details = {"lon":lon, "lat":lat, "el":el}
        new_srcs_geodetic = self.api.get_ephem(observer_details, self.srcs[:n_srcs], inplace=False)
        lon, lat, el = '148.980057138', '-35.403983527', 688.867
        observer_details = {"lon":lon, "lat":lat, "el":el}
        new_srcs_geocentric = self.api.get_ephem(observer_details, self.srcs[:n_srcs], inplace=False)
        for i in range(n_srcs):
            self.assertTrue(np.allclose(new_srcs_geodetic[i]['AZ'], new_srcs_geocentric[i]['AZ'], atol=atol))
            self.assertTrue(np.allclose(new_srcs_geodetic[i]['ALT'], new_srcs_geocentric[i]['ALT'], atol=atol))



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

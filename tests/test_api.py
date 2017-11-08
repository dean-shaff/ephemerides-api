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

    def test_get_ephem(self):
        api = EphemAPI()
        logger = logging.getLogger("TestAPI.test_get_ephem")
        n_srcs, atol = 50, 1e-3
        lon, lat, el = -211.019942862, -35.403983527 , 688.867
        observer_details = {"lon":lon, "lat":lat, "el":el}
        new_srcs_geodetic = api.get_ephem(observer_details, self.srcs[:n_srcs], inplace=False)
        lon, lat, el = '148.980057138', '-35.403983527', 688.867
        observer_details = {"lon":lon, "lat":lat, "el":el}
        new_srcs_geocentric = api.get_ephem(observer_details, self.srcs[:n_srcs], inplace=False)
        for i in range(n_srcs):
            self.assertTrue(np.allclose(new_srcs_geodetic[i]['AZ'], new_srcs_geocentric[i]['AZ'], atol=atol))
            self.assertTrue(np.allclose(new_srcs_geodetic[i]['ALT'], new_srcs_geocentric[i]['ALT'], atol=atol))

    def test_app_get_ephem(self):
        """
        Make sure we can send data to API.
        """
        logger = logging.getLogger("TestApp.test_app_get_ephem")
        n_srcs = 10
        app, api = EphemAPI.create_flask_app(__name__)
        app.testing = True
        lon, lat, el = -211.019942862, -35.403983527 , 688.867
        observer_details = {"lon":lon, "lat":lat, "el":el}
        with app.test_client() as test_app:
            rv = test_app.post("/get_ephem",
                                data=json.dumps({"observer_details":observer_details,
                                                 "sources":self.srcs[:10]}),
                                content_type="application/json")
            logger.debug(json.loads(rv.data.decode("utf-8")))
            logger.debug(rv.status_code)
            self.assertTrue(rv.status_code == 200)

    def test_app_get_ephem_error(self):
        """
        Make sure API raises correct error when data is missing or incomplete.
        """
        logger = logging.getLogger("TestApp.test_app_get_ephem_error")
        app,api = EphemAPI.create_flask_app(__name__)
        app.testing = True
        with app.test_client() as test_app:
            rv = test_app.post("/get_ephem",
                                data={})
            self.assertTrue(rv.status_code == 500)
            rv = test_app.post("/get_ephem",
                                data=json.dumps({"observer_details":{}}),
                                content_type="application/json")
            self.assertTrue(rv.status_code == 500)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()

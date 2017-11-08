import unittest
import logging

from src.api import EphemAPI

class TestApp(unittest.TestCase):

    def setUp(self):
        app, api = EphemAPI.create_flask_app(__name__)
        app.testing = True
        self.app = app.test_client()

    def test_ephem(self):
        logger = logging.getLogger("TestApp.test_ephem")
        resp = self.app.get("/get_ephem")
        logger.debug(resp.data)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

import logging
import math
import datetime

from flask import Flask
import ephem

module_logger = logging.getLogger(__name__)

class EphemAPI(object):

    methods = {
        "/get_ephem":"process_ephem_request"
    }

    def __init__(self):
        self.observer = ephem.Observer()
        self.observer.epoch = ephem.J2000

    def process_ephem_request(self):
        pass

    def get_ephem(self, observer_details, sources, inplace=True):
        """
        Given some information about the "observer" (borrowing
        from PyEphem nomenclature), or the place on earth from
        which we are looking at sources, calculate the az, el, and
        ra and dec of the sources in the sources list.

        Args:
            observer_details (dict): Details about the observer, namely
                the longitude ('lon'), latitude ('lat'), and elevation ('el').
                Longitude and Latitude should be given in degrees, as they
                will be transformed to radians.
            sources (list): A list of sources. Each source in the list should
                be a dictionary, with (at minimum) the following fields:
                    "RAJ2000": The J2000 RA in degrees
                    "DECJ2000": The J2000 DEC in degrees
        Keyword Args:
            inplace (bool): If True, we modify the source argument in place,
                if False, then we create copies of each of the entries.
        Returns:
            list: sources list, updated with new fields, namely
                "RA": The current RA,
                "DEC": The current declination,
                "AZ": The current azimuth of the source.
                "ALT": The current altitude, or elevation of the source.
        """
        lon, lat, el = observer_details['lon'], observer_details['lat'], observer_details['el']
        self.observer.lon = float(lon) * (math.pi/180.)
        self.observer.lat = float(lat) * (math.pi/180.)
        self.observer.elevation = el
        self.observer.date = datetime.datetime.utcnow()
        sources_new = []
        for src in sources:
            raJ2000, decJ2000 = src["RAJ2000"], src["DECJ2000"]
            src_body = ephem.FixedBody()
            src_body._ra = raJ2000 * (math.pi/180.)
            src_body._dec = decJ2000 * (math.pi/180.)
            src_body._epoch = ephem.J2000
            src_body.compute(self.observer)
            if not inplace:
                src_new = dict(src)
                src_new["RA"] = float(src_body.ra) * (180./math.pi)
                src_new["DEC"] = float(src_body.dec) * (180./math.pi)
                src_new["AZ"] = float(src_body.az) * (180./math.pi)
                src_new["ALT"] = float(src_body.alt) * (180./math.pi)
                sources_new.append(src_new)
                module_logger.debug("get_ephem: AZ: {}, ALT: {}, name: {}".format(
                    src_new['AZ'], src_new["ALT"], src_new.get("name", None))
                )
            elif inplace:
                src["RA"] = float(src_body.ra) * (180./math.pi)
                src["DEC"] = float(src_body.dec) * (180./math.pi)
                src["AZ"] = float(src_body.az) * (180./math.pi)
                src["ALT"] = float(src_body.alt) * (180./math.pi)
                module_logger.debug("get_ephem: AZ: {}, ALT: {}, name: {}".format(
                    src['AZ'], src["ALT"], src.get("name", None))
                )
        if inplace:
            return sources
        else:
            return sources_new

    @classmethod
    def create_flask_app(cls, name):
        api = cls()
        app = Flask(name)
        for key in cls.methods:
            app.route(key)(getattr(api, cls.methods[key]))
        return app, api

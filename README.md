## API for calculating ephemerides

This package uses PyEphem to calculate the position of objects in the sky
given some current location on the earth. Simply provide the location where
you'd like to calculate the position of the object, and the J2000 Ra and Dec
of the object in question, and the API returns the current Ra and Dec, and the
current Azimuth and Elevation at the location. 

import datetime
from rocketpy import Environment, Rocket, SolidMotor, Flight


tomorrow = datetime.date.today() + datetime.timedelta(days=1)

# Environment for Forecast launch
Env = Environment(
    railLength=5.2,
    latitude=32.990254,
    longitude=106.974998,
    elevation=1400,
    #datum='WGS84'

)

Env.setDate((tomorrow.year, tomorrow.month, tomorrow.day, 12))  # Hour given in UTC time

# Tomorrow's data. Fix this dynamically later since RocketPy seems to prefer URLs for opendap
DATA_URL = 'http://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs20230322/gfs_0p25_06z'

DICTIONARY_TYPE = ['NOAA', 'ECMWF'] # This library only supports these two types for now


Env.setAtmosphericModel(type='Forecast', file=DATA_URL, dictionary=DICTIONARY_TYPE[0])


Env.info()

'''
Env.info() should output similar info as follows - 

Launch Site Details

Launch Rail Length: 5.2  m
Launch Date: 2023-03-24 12:00:00 UTC
Launch Site Latitude: 32.99025°
Launch Site Longitude: 106.97500°
Reference Datum: SIRGAS2000
Launch Site UTM coordinates: 684531.36 E    3651938.65 N
Launch Site UTM zone: 48S
Launch Site Surface Elevation: 688.5 m


Atmospheric Model Details

Atmospheric Model Type: Forecast
Forecast Maximum Height: 79.264 km
Forecast Time Period: From  2023-03-22 06:00:00  to  2023-04-07 06:00:00  UTC
Forecast Hour Interval: 3  hrs
Forecast Latitude Range: From  -90.0 ° To  90.0 °
Forecast Longitude Range: From  0.0 ° To  359.75 °


Surface Atmospheric Conditions

Surface Wind Speed: 4.32 m/s
Surface Wind Direction: 42.19°
Surface Wind Heading: 222.19°
Surface Pressure: 940.35 hPa
Surface Temperature: 281.89 K
Surface Air Density: 1.162 kg/m³
Surface Speed of Sound: 336.57 m/s
'''




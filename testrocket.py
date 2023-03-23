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



Pro75M1670 = SolidMotor(
    thrustSource="data/motors/Cesaroni_M1670.eng", # Reference sample data in this repo
    burnOut=3.9,
    grainNumber=5,
    grainSeparation=5 / 1000,
    grainDensity=1815,
    grainOuterRadius=33 / 1000,
    grainInitialInnerRadius=15 / 1000,
    grainInitialHeight=120 / 1000,
    nozzleRadius=33 / 1000,
    throatRadius=11 / 1000,
    interpolationMethod="linear",
)


Pro75M1670.info()

'''
Motor Details
Total Burning Time: 3.9 s
Total Propellant Mass: 2.956 kg
Propellant Exhaust Velocity: 2038.745 m/s
Average Thrust: 1545.218 N
Maximum Thrust: 2200.0 N at 0.15 s after ignition.
Total Impulse: 6026.350 Ns
'''


# Add a test rocket

Calisto = Rocket(
    motor=Pro75M1670,
    radius=127 / 2000,
    mass=19.197 - 2.956,
    inertiaI=6.60,
    inertiaZ=0.0351,
    distanceRocketNozzle=-1.255,
    distanceRocketPropellant=-0.85704,
    powerOffDrag="data/calisto/powerOffDragCurve.csv",
    powerOnDrag="data/calisto/powerOnDragCurve.csv",
)

Calisto.setRailButtons([0.2, -0.5])


NoseCone = Calisto.addNose(length=0.55829, kind="vonKarman", distanceToCM=0.71971)

FinSet = Calisto.addTrapezoidalFins(
    n=4,
    rootChord=0.120,
    tipChord=0.040,
    span=0.100,
    distanceToCM=-1.04956,
    cantAngle=0,
    radius=None,
    airfoil=None,
)

Tail = Calisto.addTail(
    topRadius=0.0635, bottomRadius=0.0435, length=0.060, distanceToCM=-1.194656
)


def drogueTrigger(p, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate drogue when vz < 0 m/s.
    return True if y[5] < 0 else False


def mainTrigger(p, y):
    # p = pressure
    # y = [x, y, z, vx, vy, vz, e0, e1, e2, e3, w1, w2, w3]
    # activate main when vz < 0 m/s and z < 800 + 1400 m (+1400 due to surface elevation).
    return True if y[5] < 0 and y[2] < 800 + 1400 else False


Main = Calisto.addParachute(
    "Main",
    CdS=10.0,
    trigger=mainTrigger,
    samplingRate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)


Drogue = Calisto.addParachute(
    "Drogue",
    CdS=1.0,
    trigger=drogueTrigger,
    samplingRate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

'''
If the above addParachute function is ran multiple times, it will add multiple parachutes. 
Can be removed with - 
Calisto.parachutes.remove(Drogue)
Calisto.parachutes.remove(Main)
'''


TestFlight = Flight(rocket=Calisto, environment=Env, inclination=85, heading=0)


# Get all launch/flight information.
TestFlight.allInfo()

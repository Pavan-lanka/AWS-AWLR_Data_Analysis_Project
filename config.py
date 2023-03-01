from datetime import datetime as dt

STATION_ID = 'station_id'
START_TIME = 'start_time'
END_TIME = dt('end_time')
OBS_FREQUENCY = 'obs_frequency'
TEMPERATURE = float('temperature')
WIND_SPEED = 'wind_speed'
WIND_DIRECTION = int('wind_direction')
VISIBILITY = 'visibility'
PRESENT_WEATHER = 'present_weather'
DEW_POINT_TEMPERATURE = float('dew_point_temperature')
CLOUD_TYPE = 'cloud_type'
CLOUD_BASE = 'cloud_base'
PRECIPITATION = 'precipitation'
ATOMIC_PRESSURE = 'atomic_pressure'
TOTAL_AMOUNT_OF_CLOUDS = 'total_amount_of_clouds'

REQUIRED_PARAMETERS = [TEMPERATURE, WIND_SPEED, WIND_DIRECTION,
                       ATOMIC_PRESSURE, PRESENT_WEATHER, START_TIME,
                       END_TIME, OBS_FREQUENCY, STATION_ID]

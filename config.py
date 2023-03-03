from datetime import datetime as dt

STATION_ID = 'station_id'
START_TIME = 'start_time'
END_TIME = 'end_time'
OBS_FREQUENCY = 'obs_frequency'
TEMPERATURE = 'temperature'
DEWPOINT = 'dewpoint'
WIND_SPEED = 'wind_speed'
WIND_DIRECTION = 'wind_direction'
CLOUD_HEIGHT = 'pressure'
PRESSURE = 'cloud_height'
HIGH_CLOUD = 'high_cloud'
MID_CLOUD = 'mid_cloud'
LOW_CLOUD = 'low_cloud'
SKY_COVER = 'sky_cover'
VISIBILITY_DISTANCE = 'visibility_distance'
PRESENT_WEATHER = 'present_weather'
PAST_WEATHER = 'past_weather'
PRESSURE_TENDENCY = 'pressure_tendency'
PRESSURE_CHANGE = 'pressure_change'
PRESSURE_DIFFERENCE = 'pressure_difference'
PRECIPITATION = 'precipitation'
SKY_COVER_AT_LOWEST_CLOUD = 'sky_cover_at_lowest_cloud'


REQUIRED_PARAMETERS = [TEMPERATURE, WIND_SPEED, WIND_DIRECTION,
                       PRESSURE, PRESENT_WEATHER, START_TIME,
                       END_TIME, OBS_FREQUENCY, STATION_ID]

import metpy.plots as plots
from metpy.units import units
import matplotlib.pyplot as plt
import xarray as xr
from metpy.io import *
import pandas as pd
import meteostat as mt
from datetime import datetime as dt
from metpy.cbook import get_test_data


class FetchData:

    def __init__(self, station_id: str = None, path_to_file: str = None):
        self.station_id = station_id
        self.path_to_file = path_to_file

        '''FetchData Method takes Station_ID as String. ex:'12992'
        start is Start time for accumulation of observations in dt format. ex_Input: dt(YYYY, MM, DD, HH, MM, SS)
        end is End time range of the accumulation of data in dt format . dt(YYYY, MM, DD, HH, MM, SS) 
                                                                        -> (2022,  1,  2, 23, 59)
        period is observation frequency for the observations. parameter only accepts string Ex. 'Monthly','Hourly','Daily'
        Example input: 
        FetchData('43128', dt(2022, 1, 1), dt(2022, 1, 1, 23, 59), 'daily')
        # a = FetchData('43128')
        # a = a.fetch_station_data(dt(2022, 1, 1), dt(2022, 1, 1, 23, 59), 'hourly')
        '''

    def fetch_station_data(self, start_time: dt, end_time: dt, obs_frequency: str):
        if obs_frequency.lower() == 'hourly':
            if start_time > end_time:
                print('Enter Valid date time to fetch hourly data')
            else:
                data = mt.Hourly(self.station_id, start_time, end_time)
                data = data.fetch()
                return data
        elif obs_frequency.lower() == 'daily':
            if start_time > end_time or start_time == end_time:
                print('Enter Valid days for fetching Daily data')
            else:
                data = mt.Daily(self.station_id, start_time, end_time)
                data = data.fetch()
                return data
        elif obs_frequency.lower() == 'monthly':
            if start_time > end_time or start_time == end_time:
                print('Enter Valid months in Date,Time for fetching monthly data')
            else:
                data = mt.Monthly(self.station_id, start_time, end_time)
                data = data.fetch()
                return data
        else:
            return print('The data period frequency is not valid')

    def custom_file_read(self):
        """This method takes the '.CSV' file or File_Path as input parameter and returns DF from
        # a= CustomData('pa1.csv')
        # a = a.custom_file_read()
        # print(a)
        """
        if self.path_to_file[-4:] == '.csv':
            data = pd.read_csv(self.path_to_file)
            return data
        elif self.path_to_file[-4:] == '.txt' and self.path_to_file[:5].lower() == 'metar':
            data = parse_metar_to_dataframe(filename=self.path_to_file)
            return data
        elif self.path_to_file[-3:] == '.nc':
            data = xr.open_dataset(self.path_to_file).parse_cf()
            return data

# class Parameters:
#
#     def __init__(self, data: list):
#         self.PATH_TO_FILE = None
#         CustomData(PATH_TO_FILE).custom_file_read()
#
#
#     def read_parameters(self, ):
#         parameters = {
#             'STATION_ID': ['station_id',],
#             'START_TIME': 'start_time',
#             'END_TIME': 'end_time',
#             'OBS_FREQUENCY': 'obs_frequency',
#             'HUMIDITY': 'humidity',
#             'TEMPERATURE': 'temperature',
#             'DEWPOINT': 'dew_point',
#             'WIND_SPEED': 'wspd',
#             'WIND_DIRECTION': 'wind_direction',
#             'CLOUD_HEIGHT': 'cloud_height',
#             'PRESSURE': 'pressure',
#             'HIGH_CLOUD': 'high_cloud',
#             'MID_CLOUD': 'mid_cloud',
#             'LOW_CLOUD': 'low_cloud',
#             'SKY_COVER': 'sky_cover',
#             'VISIBILITY_DISTANCE': 'visibility_distance',
#             'PRESENT_WEATHER': 'present_weather',
#             'PAST_WEATHER': 'past_weather',
#             'PRESSURE_TENDENCY': 'press_tendency',
#             'PRESSURE_CHANGE': 'pressure_change',
#             'PRESSURE_DIFFERENCE': 'pressure_difference',
#             'PRECIPITATION': 'precipitation',
#             'SKY_COVER_AT_LOWEST_CLOUD': 'sky_cover_at_lowest_cloud',
#         }
# class Abbreviations:
#     def abbreviations(self):
#         low_cloud = {('SKY_CLEAR', 'SKC'): 0,
#                      ('CUMULUS', 'CU'): 1,
#                      ('CUMULUS', 'TCU'): 2,
#                      ('CUMULONIMBUS', 'CB'): 3,
#                      ('STRATOCUMULUS', 'SCCU'): 4,
#                      ('STRATOCUMULUS', 'SC'): 5,
#                      ('STRATUS', 'ST'): 6,
#                      ('FRACTOSTRATUS', 'STFRA'): 7,
#                      ('CUMULUS_AND_STRATOCUMULUS', 'CUSU'): 8,
#                      ('CUMULONIMBUS', 'CB'): 9}
#
#         high_cloud = {('SKY_CLEAR', 'SKC'): 0,
#                       ('CIRROCUMULUS', 'CC'): 9,
#                       ('CIRROSTRATUS', 'CS'): 8,
#
#
#
#
#
#
#         }

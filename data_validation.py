import config
import metpy.plots as plots
from metpy.units import units
import matplotlib.pyplot as plt
import pandas as pd
import meteostat as mt
from datetime import datetime as dt

class FetchData:

    def __init__(self, station_id: str, start_time: dt, end_time: dt, obs_frequency: str):
        self.station_id = station_id
        self.start_time = start_time
        self.end_time = end_time
        self.obs_frequency = obs_frequency
        '''FetchData Method takes Station_ID as String. ex:'12992'
        start is Start time for accumulation of observations in dt format. ex_Input: dt(YYYY, MM, DD, HH, MM, SS)
        end is End time range of the accumulation of data in dt format . dt(YYYY, MM, DD, HH, MM, SS) 
                                                                        -> (2022,  1,  2, 23, 59)
        period is observation frequency for the observations. parameter only accepts string Ex. 'Monthly','Hourly','Daily'
        Example input: 
        FetchData('43128', dt(2022, 1, 1), dt(2022, 1, 1, 23, 59), 'daily')
        '''

    def fetch_station_data(self):
        if self.obs_frequency.lower() == 'hourly':
            if self.start_time > self.end_time:
                print('Enter Valid date time to fetch hourly data')
            else:
                data = mt.Hourly(self.station_id, self.start_time, self.end_time)
                data = data.fetch()
                return data
        elif self.obs_frequency.lower() == 'daily':
            if self.start_time > self.end_time or self.start_time == self.end_time:
                print('Enter Valid days for fetching Daily data')
            else:
                data = mt.Daily(self.station_id, self.start_time, self.end_time)
                data = data.fetch()
                return data
        elif self.obs_frequency.lower() == 'monthly':
            if self.start_time > self.end_time or self.start_time == self.end_time:
                print('Enter Valid months in Date,Time for fetching monthly data')
            else:
                data = mt.Monthly(self.station_id, self.start_time, self.end_time)
                data = data.fetch()
                return data
        else:
            return print('The data period frequency is not valid')


class CustomData:
    def __init__(self, PATH_TO_FILE):
        self.PATH_TO_FILE = PATH_TO_FILE

    def custom_file_read(self, csvreader):
        if self.PATH_TO_FILE[-4:] == '.csv':
            csvreader = pd.read_csv(self.PATH_TO_FILE)
            return csvreader
        elif self.PATH_TO_FILE[-4:] != '.csv':
            return print('Please enter path to CSV file or a dataframe')


class Station:
    def __init__(self, ):


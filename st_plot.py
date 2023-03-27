from metpy.plots import *
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from metpy.io import *
import pandas as pd
import meteostat as mt
from datetime import datetime as dt
from dataclasses import dataclass
import metpy


@dataclass
class FetchData:
    station_id: str = None
    path_to_file: str = None
    '''FetchData Method takes Station_ID as String. ex:'12992'
    start is Start time for accumulation of observations in dt format. ex_Input: dt(YYYY, MM, DD, HH, MM, SS)
    end is End time range of the accumulation of data in dt format . dt(YYYY, MM, DD, HH, MM, SS) 
                                                                    -> (2022,  1,  2, 23, 59)
    period is observation frequency for the observations. parameter only accepts string, defaults to 'Hourly'
    Ex. 'Monthly','Daily'
    Example input:
    # a = FetchData('43128')
    # a = a.fetch_station_data(dt(2022, 1, 1), dt(2022, 1, 1, 23, 59), 'hourly')
    '''

    def fetch_station_data(self, start_time: dt, end_time: dt, obs_frequency='hourly'):
        if obs_frequency.lower() == 'hourly':
            if start_time >= end_time:
                print('Enter Valid date time to fetch hourly data')
            else:
                data = mt.Hourly(self.station_id, start_time, end_time)
                data = data.fetch()
                d_parameters = list(data.columns.values)
                return data, d_parameters
        elif obs_frequency.lower() == 'daily':
            if start_time >= end_time:
                print('Enter Valid days for fetching Daily data')
            else:
                data = mt.Daily(self.station_id, start_time, end_time)
                data = data.fetch()
                d_parameters = list(data.columns.values)
                return data, d_parameters
        elif obs_frequency.lower() == 'monthly':
            if start_time >= end_time:
                print('Enter Valid months in Date,Time for fetching monthly data')
            else:
                data = mt.Monthly(self.station_id, start_time, end_time)
                data = data.fetch()
                d_parameters = list(data.columns.values)
                return data, d_parameters
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
            d_parameters = list(data.columns.values)
            return data, d_parameters
        elif '.txt' in self.path_to_file[-4:]:
            data = parse_metar_file(filename=self.path_to_file)
            d_parameters = list(data.columns.values)
            return data, d_parameters
        elif self.path_to_file[-4:] == '.xml':
            data = pd.read_xml(path_or_buffer=self.path_to_file)
            d_parameters = list(data.columns.values)
            return data, d_parameters
        elif self.path_to_file[-3:] == '.cn':
            data = xr.open_dataset(filename_or_obj=self.path_to_file, engine="netcdf4")
            data = data.metpy.parse_cf()
            data = data.to_dataframe()
            data = data.reset_index()
            d_parameters = list(data.columns.values)
            return data, d_parameters
        else:
            print('File Format should be a .csv, .txt, .cn(X-array Dataset) or .xml file')

    @staticmethod
    def get_input():
        ts_str = input("Enter a timestamp in the format 'YYYY-MM-DD HH:MM:SS': ")
        ts = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
        return ts

    @staticmethod
    def param_data_validation(self, a, b=custom_file_read(), ip = get_input()):
        parameter_abbreviations = {
            'station_id':['Station_ID','station', 'station_id' ],
            'date_time': ['valid', 'time', 'date_time'],

            'temperature': ['Temperature', 'TEMPERATURE', 'tmpt', 'air_temperature',
                            'temp', 'tmpf', 'tmpc', 'temperature'],
            'dew_point_temperature': ['Dew_Point_Temperature', 'DEW_POINT_TEMPERATURE', 'dwpt', 'dwpc',
                                      'dew_temp', 'dwpf', 'dew_point_temperature'],
            'wind_speed': ['WIND_SPEED', 'wspd', 'sknt', 'Wind_Speed', 'wind_speed'],
            'wind_direction': ['WIND_DIRECTION', 'Wind_Direction', 'drct', 'wdir', 'wind_direction'],
            'cloud_height': ['skyl3', 'highest_cloud_level', 'high_cloud_level',
                             'medium_cloud_level', 'low_cloud_level'],
            'pressure': ['PRESSURE', 'pres', 'mslp', 'atmospheric_pressure', 'air_pressure_at_sea_level'],
            'high_cloud': ['high_cloud_type', 'skyc3', 'high_cloud'],
            'mid_cloud': ['mid_cloud_type', 'skyc2', 'mid_cloud'],
            'low_cloud': ['low_cloud_type', 'skyc1','low_cloud'],
            'sky_cover': ['cloud_coverage', 'skyc1','sky_cover'],
            'visibility_distance': ['visibility', 'vsby','visibility_distance'],
            'present_weather': ['coco', 'current_weather', 'wxcodes', 'current_wx1','present_weather'],
            'past_weather': None,
            'pressure_tendency': None,
            'pressure_change': None,
            'pressure_difference': None,
            'precipitation': ['p01i', 'prcp', 'PRECIPITATION', 'precipitation'],
            'sky_cover_at_lowest_cloud': ['low_cloud_level', 'skyl1',
                                          'SKY_COVER_AT_LOWEST_CLOUD', 'sky_cover_at_lowest_cloud']
        }
        data = {}
        for i in range(len(b)):
            for key, tuple_keys in parameter_abbreviations:
                if b[i] in parameter_abbreviations:
                    data[b[i]] = a.
                elif b[i] not in parameter_abbreviations:
                    for j in tuple_keys:




# a = FetchData(path_to_file=r"C:\Users\Pavan Koundinya\Desktop\metar_vij.txt")
# a, b = a.custom_file_read()
# an = list(a.columns.values)
# print(an)


@dataclass()
class StationModel:
    sp = None
    ax = None
    data = {
        # 'temperature': None,
        # 'dew_point_temperature': None,
        # 'wind_speed': None,
        # 'wind_direction': None,
        # 'cloud_height': None,
        # 'pressure': None,
        # 'high_cloud': None,
        # 'mid_cloud': None,
        # 'low_cloud': None,
        # 'sky_cover': None,
        # 'visibility_distance': None,
        # 'present_weather': None,
        # 'past_weather': None,
        # 'pressure_tendency': None,
        # 'pressure_change': None,
        # 'pressure_difference': None,
        # 'precipitation': None,
        # 'sky_cover_at_lowest_cloud': None
    }

    def plot_station_model(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
        self.sp = StationPlot(ax, 0, 0, fontsize=13, spacing=25)
        self.ax.set_title('Station Model')
        station_circle = patches.Circle((0, 0), radius=7, lw=1, edgecolor='k', facecolor='w')
        self.ax.add_patch(station_circle)
        # to add pressure_tendency symbol to the model
        self.sp.plot_symbol((5, 0), codes=[self.data['pressure_tendency']], symbol_mapper=pressure_tendency,
                            va='center', ha='center', fontsize=25)

        # to add Sky_cover symbol to the model
        self.sp.plot_symbol((0, 0), codes=[self.data['sky_cover']], symbol_mapper=sky_cover, fontsize=25)

        # to add pressure to the model
        self.sp.plot_text((4, 3), text=[str(self.data['pressure']) + ' hPa'], fontsize=13)

        # to position wind-barb in the center of the model
        # u = -wind_speed * np.sin(np.radians(wind_direction))
        # v = -wspd_mps * math.cos(np.radians(wind_direction))
        self.sp.plot_barb(u=[-(self.data['wind_speed']) * np.sin(np.radians(self.data['wind_direction']))],
                          v=[-(self.data['wind_speed']) * np.cos(np.radians(self.data['wind_direction']))], length=11)
        # to add wind speed in knots at the end of the barb
        self.ax.text(1.5 * np.sin(np.radians(self.data['wind_direction'])),
                     1.5 * np.cos(np.radians(self.data['wind_direction'])),
                     str(self.data['wind_speed']) + ' kts',
                     ha='center', va='bottom', rotation=0, fontsize=10, alpha=0.3)

        # to add height of the cloud base
        self.sp.plot_text((-2, -5.5), text=[str(self.data['cloud_height'])], fontsize=13)

        # to add dew_point_temperature to the model
        self.sp.plot_text((-4, 3), text=[str(self.data['dew_point_temperature']) + '°C'], fontsize=13)

        # to add high_clouds symbol to the model
        self.sp.plot_symbol((1, 5), codes=[self.data['high_cloud']], symbol_mapper=high_clouds,
                            va='center', ha='center', fontsize=25)

        # to add low_clouds symbol to the model
        self.sp.plot_symbol((-2, -3.5), codes=[self.data['low_cloud']], symbol_mapper=low_clouds,
                            va='center', ha='center', fontsize=25)

        # to add mid_clouds symbol to the model
        self.sp.plot_symbol((2, 3), codes=[self.data['mid_cloud']], symbol_mapper=mid_clouds,
                            va='center', ha='center', fontsize=25)

        # to add past_weather symbol to the model
        self.sp.plot_symbol((2, -3.5), codes=wx_code_map[self.data['past_weather']], symbol_mapper=current_weather,
                            va='center', ha='center', fontsize=25)

        # to add precipitation to the model
        self.sp.plot_text((2, -5.5), text=[str(self.data['precipitation'])], fontsize=13)

        # to add present_weather symbol to the model
        self.sp.plot_symbol((-4, 0), codes=wx_code_map[self.data['present_weather']], symbol_mapper=current_weather,
                            va='center', ha='center', fontsize=25)

        # to add pressure_change to the model
        self.sp.plot_text((3.2, 0), text=[str(self.data['pressure_change'])], fontsize=13)

        # to add pressure_difference to the model
        self.sp.plot_text((4, 0), text=[str(self.data['pressure_difference'])], fontsize=13)

        # to add sky_cover_of the lowest cloud to the model
        self.sp.plot_text((0, -4), text=[str(self.data['sky_cover_at_lowest_cloud'])], fontsize=13)

        # to add temperature to the model
        self.sp.plot_text((-4, 3), text=[str(self.data['temperature']) + '°C'], fontsize=13)

        # to add visibility_distance to the model
        self.sp.plot_text((-6, 0), text=[str(self.data['visibility_distance']) + 'miles'], fontsize=13)
        return plt.show()




# adding metpy logo at the corner
# al = add_metpy_logo(fig=fig, x=8, y=8, zorder=5, size='small')

# plt.grid()

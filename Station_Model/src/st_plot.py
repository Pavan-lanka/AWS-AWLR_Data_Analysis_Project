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
import cv2
import os


@dataclass
class StationModelPlot:
    station_id: str = None
    path_to_file: str = None

    '''
    StationModelPlot Class accepts 
    Station_ID as String. ex:'12992' & 
    path_to_file as Path to file or file as object
    
    '''

    def fetch_station_data(self, start_time, end_time, obs_frequency='hourly'):
        """

        :param start_time: Start time to fetch data Ex: 2023-05-29 07:51:00
        :param end_time: End time to fetch data Ex: 2023-03-29 07:51:00
        :param obs_frequency: observation Frequency of data Ex. (Hourly, Daily)
        :return: Tuple of (CSV file, List)
                 containing CSV Data File of weather data and columns values of the data
        """
        frequency = ['hourly', 'daily']
        frequency_fetch = {'hourly': mt.Hourly,
                           'daily': mt.Daily
                           }
        if obs_frequency.lower() in frequency and start_time <= end_time:
            weather_data = frequency_fetch[obs_frequency](self.station_id, start_time, end_time)
            weather_data = weather_data.fetch()
            weather_data = weather_data.reset_index()
            data_parameters = list(weather_data.columns.values)
            return weather_data, data_parameters
        elif obs_frequency.lower() not in frequency:
            raise RuntimeError(
                f"Enter a valid observation frequency from {frequency} or Start time should be less than End time")

    def custom_file_read(self):
        """

        :return: A tuple containing Data Frame of Weather Data, list of column names
        """
        supported_types = ['nc', 'xml', 'txt', 'csv']
        extension_read = {'nc': xr.open_dataset,
                          'xml': pd.read_xml,
                          'txt': parse_metar_file,
                          'csv': pd.read_csv
                          }
        extension = self.path_to_file[self.path_to_file.rfind('.'):][1:]
        if extension not in supported_types:
            print(extension)
            print('txt' in supported_types)
            raise RuntimeError(f'Supported file formats are {supported_types}')
        elif extension == 'nc':
            weather_data = extension_read['nc'](self.path_to_file, engine="netcdf4")
            weather_data = weather_data.metpy.parse_cf()
            weather_data = weather_data.to_dataframe()
            try:
                weather_data = weather_data.reset_index()
            except Exception as e:
                weather_data = weather_data.reset_index(drop=True)
            data_parameters = list(weather_data.columns.values)
        else:
            weather_data = extension_read[extension](self.path_to_file)
            try:
                weather_data = weather_data.reset_index()
            except Exception as e:
                weather_data = weather_data.reset_index(drop=True)
            data_parameters = list(weather_data.columns.values)
        return weather_data, data_parameters

    @staticmethod
    def parameter_validation(time_stamp_data: dict, data_columns: list):
        """

        :param time_stamp_data: A dictionary of all Parameters from weather data, weather data values
        :param data_columns: A list of Weather Parameter Abbreviations
        :return: Dictionary of valid Parameter names, values to plot
        """
        data_to_plot = {}
        parameter_abbreviations = {
            'station_id': ['Station_ID', 'station', 'station_id', 'STATION_ID', 'ID', 'id'],
            'date_time': ['valid', 'time', 'date_time', 'time1', 'time_stamp', 'DATE_TIME'],

            'temperature': ['Temperature', 'TEMPERATURE', 'tmpt', 'air_temperature',
                            'temp', 'tmpf', 'tmpc', 'temperature', 'tavg'],
            'dew_point_temperature': ['Dew_Point_Temperature', 'DEW_POINT_TEMPERATURE', 'dwpt', 'dwpc',
                                      'dew_temp', 'dwpf', 'dew_point_temperature'],
            'wind_speed': ['WIND_SPEED', 'wspd', 'sknt', 'Wind_Speed', 'wind_speed'],
            'wind_direction': ['WIND_DIRECTION', 'Wind_Direction', 'drct', 'wdir', 'wind_direction'],
            'cloud_height': ['skyl1', 'skyl2', 'skyl3', 'skyl4', 'highest_cloud_level', 'high_cloud_level',
                             'medium_cloud_level', 'low_cloud_level'],
            'pressure': ['PRESSURE', 'pres', 'mslp', 'atmospheric_pressure', 'air_pressure_at_sea_level'],
            'high_cloud': ['highest_cloud_type', 'skyc3', 'high_cloud'],
            'mid_cloud': ['medium_cloud_type', 'skyc2', 'mid_cloud'],
            'low_cloud': ['low_cloud_type', 'skyc1', 'low_cloud'],
            'sky_cover': ['cloud_coverage', 'skyc1', 'sky_cover'],
            'visibility_distance': ['visibility', 'vsby', 'visibility_distance'],
            'present_weather': ['coco', 'current_weather', 'wxcodes', 'current_wx1', 'current_wx1_symbol',
                                'present_weather'],
            'past_weather': [],
            'pressure_tendency': [],
            'pressure_change': [],
            'pressure_difference': [],
            'precipitation': ['p01i', 'prcp', 'PRECIPITATION', 'precipitation'],
            'sky_cover_at_lowest_cloud': ['SKY_COVER_AT_LOWEST_CLOUD', 'sky_cover_at_lowest_cloud',
                                          'cloud_coverage', 'skyl1']
        }
        parameter_keys = list(parameter_abbreviations.keys())
        parameter_abb_list = list(parameter_abbreviations.values())
        parameters_values = []
        not_available_parameters = list()
        for abbrv_list in parameter_abb_list:
            for abbrvs in abbrv_list:
                parameters_values.append(abbrvs)
        for iteration in data_columns:
            if iteration in parameter_keys:
                data_to_plot[iteration] = time_stamp_data[iteration]
            elif iteration not in parameter_keys:
                if iteration in parameters_values:
                    for key, value in parameter_abbreviations.items():
                        if iteration in value:
                            index_key = key
                            data_to_plot[index_key] = time_stamp_data[iteration]
                elif iteration not in parameters_values:
                    not_available_parameters.append(iteration)

        if len(not_available_parameters) > 0:
            user_parameter = input(f"parameter abbreviations {not_available_parameters} "
                                   f"are not recognized to plot data, Please select the "
                                   f"parameter from {parameter_keys} to add an abbreviation:\t")
            if user_parameter in parameter_keys:
                user_added_abbreviation = input('Enter abbreviation for the selected parameter:\t')
                parameter_abbreviations[user_parameter].append(user_added_abbreviation)
            else:
                print(f"Parameters {not_available_parameters} cannot be plotted in the Station model")
        return data_to_plot

    @staticmethod
    def plot_station_model(data: dict):
        """

        :param data: A dictionary containing data to plot into Station Model
        :return: Path to Image containing Station Model
        """
        fig, ax = plt.subplots(figsize=(10, 10))
        sp = StationPlot(ax, 0, 0, fontsize=18, spacing=25)
        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        ax.set_title('Station Model', fontsize=22, bbox=dict(boxstyle='square', facecolor='white', alpha=0.3)
                     , weight='heavy', family='monospace')
        station_square = plt.Rectangle((-6, -6), 12, 12, fc='white', ec="k")
        # ax.set_aspect()
        ax.add_patch(station_square)
        plot_dictionary = {
            # to add pressure_tendency symbol to the model
            'pressure_tendency': "sp.plot_symbol((6, 0.3), codes=[data['pressure_tendency']],"
                                 "symbol_mapper=pressure_tendency,va='center', ha='center', fontsize=25)",

            # to add Sky_cover symbol to the model
            'sky_cover': "sp.plot_symbol((0, 0), codes=[data['sky_cover']], symbol_mapper=sky_cover, fontsize=25)",

            # to add pressure to the model
            'pressure': "ax.text(3, 2, s=str(round(data['pressure'])) + ' hPa', fontsize=13)",

            # to position wind-barb in the center of the model
            # u = [-wind_speed * np.sin(np.radians(wind_direction))] U component of wind barb
            # v = [-wspd_mps * math.cos(np.radians(wind_direction))] V component of wind barb
            'wind_speed': "sp.plot_barb(u=[-(data['wind_speed']) * np.sin(np.radians(data['wind_direction']))],"
                          "v=[-(data['wind_speed']) * np.cos(np.radians(data['wind_direction']))], length=10)",
            # to add wind speed in knots at the end of the barb
            'wind_direction': "ax.text(-1 * np.sin(np.radians(data['wind_direction'])),"
                              "-1 * np.cos(np.radians(data['wind_direction'])),str(data['wind_speed']) + ' kts',"
                              "ha='center', va='bottom', fontsize=10, alpha=0.3)",

            # to add height of the cloud base
            'cloud_height': "ax.text(-2, -3.5, s=str(data['cloud_height']), fontsize=13)",

            # to add dew_point_temperature to the model
            'dew_point_temperature': "ax.text(-3.5, -3, "
                                     "s=str(data['dew_point_temperature']) + '°C', fontsize=13)",

            # to add high_clouds symbol to the model
            'high_cloud': "ax.text(1.5, 4, s = str(data['high_cloud']), fontsize=13,"
                          " bbox=dict(boxstyle='round',facecolor='turquoise', alpha=0.7))",

            # to add low_clouds symbol to the model
            'low_cloud': "ax.text(-1.7, -3, s = str(data['low_cloud']), fontsize=13,"
                         "bbox=dict(boxstyle='round',facecolor='turquoise', alpha=0.2))",

            # to add mid_clouds symbol to the model
            'mid_cloud': "ax.text(1.5, 2, s = str(data['mid_cloud']), fontsize=13, "
                         "bbox=dict(boxstyle='round',facecolor='turquoise', alpha=0.5))",

            # to add past_weather symbol to the model
            'past_weather': "sp.plot_symbol((2, -3.5), codes=[int(data['past_weather'])], "
                            "symbol_mapper=current_weather,va='center', ha='center', fontsize=25) ",

            # to add precipitation to the model
            'precipitation': "sp.plot_text((2, -5.5), text=[str(data['precipitation'])], fontsize=13)",

            # to add present_weather symbol to the model
            'present_weather': "sp.plot_symbol((-3.5, 0), codes=[int(data['present_weather'])], "
                               "symbol_mapper=current_weather,va='center', ha='center', fontsize=25)",

            # to add pressure_change to the model
            'pressure_change': "ax.text(3, 0, s=str(data['pressure_change']), fontsize=15, weight='bold')",

            # to add pressure_difference to the model
            'pressure_difference': "ax.text(3.5, 0, s=str(data['pressure_difference']), fontsize=13)",

            # to add sky_cover_of the lowest cloud to the model
            'sky_cover_at_lowest_cloud': "ax.text(-0.2, -3, "
                                         "s=str(data['sky_cover_at_lowest_cloud']), fontsize=13)",

            # to add temperature to the model
            'temperature': "ax.text(-3.5, 2, s = str(data['temperature'])+'°C', fontsize=13)",

            # to add visibility_distance to the model
            'visibility_distance': "ax.text(-4.5, 0, s=str(round(data['visibility_distance'])), fontsize=13)",

            # adds Station_ID to the model
            'station_id': "ax.text(2.8, 6.7, "
                          "s =('Station ID: ' + data['station_id']), fontsize=13)",

            'date_time': "ax.text(-0.5, 6.2, "
                         "s = ('Date & Time:' + '' + str(data['date_time']).rstrip('Timestamp()'))"
                         ", fontsize = 13)"
        }
        for key, value in data.items():
            if key in plot_dictionary:
                eval(plot_dictionary[key])

        name = 'Station_model.jpeg'
        path = os.path.join(os.path.dirname('output'), name)
        plt.axis('off')
        plt.savefig(path, dpi=100)

        return path

    @staticmethod
    def get_time_stamp(time_stamp_string):
        """get_time_stamp method accepts argument as String in the format --> 'YYYY-MM-DD HH:MM' """
        if len(time_stamp_string) == 16:
            ts = dt.strptime(time_stamp_string, '%Y-%m-%d %H:%M')
        elif len(time_stamp_string) == 19:
            ts = dt.strptime(time_stamp_string, '%Y-%m-%d %H:%M:%S')
        return ts

    def _get_pressure_change_symbol(p_curr, p_prev):

        pressure_diff = p_curr - p_prev
        if pressure_diff > 0:
            return '-'
        elif pressure_diff < 0:
            return '+'
        return '±', pressure_diff

    @staticmethod
    def press_values(pressure_dict: dict):
        """"""
        pressure_tend = -1
        pressure_change_symbol = ''
        if len(pressure_dict) == 4:
            p4 = pressure_dict[3]
            p3 = pressure_dict[2]
            p2 = pressure_dict[1]
            p1 = pressure_dict[0]
            pressure_change_symbol, pressure_diff = StationModelPlot._get_pressure_change_symbol(p1, p4)
            if p1 >= p4 and (p3 - p4 >= 3 and p2 - p3 >= 3):
                pressure_tend = 0
            elif p1 - p4 >= 1 and (p1 - p2 < 3 and p2 - p3 < 3):
                pressure_tend = 1
            elif (p1 - p4 > 3 and (p1 - p2 > 3 and p2 - p3 > 3)) or p4 < p3 < p2 < p1:
                pressure_tend = 2
            elif p1 - p4 > 1 and (p1 - p2 >= 3 and p3 - p2 >= 3):
                pressure_tend = 3
            elif (p4 == p3 == p2 == p1) or abs(p1 - p4) <= 1:
                pressure_tend = 4
            elif p1 <= p4 and (p4 - p3 >= 3 and p3 - p2 >= 3):
                pressure_tend = 5
            elif p4 - p1 > 1 and (p1 - p2 <= 1 and p2 - p3 <= 1):
                pressure_tend = 6
            elif (p4 - p1 > 3 and (p2 - p1 >= 3 and p3 - p2 >= 3 and p4 - p3 >= 3)) or p4 > p3 > p2 > p1:
                pressure_tend = 7
            elif p4 - p1 > 1 and (p2 - p1 >= 3 and p3 - p2 >= 3):
                pressure_tend = 8

            return pressure_change_symbol, abs(int(pressure_diff)), pressure_tend
        else:
            return pressure_change_symbol, pressure_diff

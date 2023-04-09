import warnings
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
import pickle


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
    def parameter_validation(time_stamp_data: dict, data_columns: list, parameter_abbreviations: dict):
        """

        :param parameter_abbreviations: A dictionary containing parameter abbreviations
        :param time_stamp_data: A dictionary of all Parameters from weather data, weather data values
        :param data_columns: A list of Weather Parameter Abbreviations
        :return: Dictionary of valid Parameter names, values to plot
        """
        data_to_plot = dict()
        parameter_keys = list(parameter_abbreviations.keys())
        parameter_abb_list = list(parameter_abbreviations.values())
        parameters_values = []
        not_available_parameters = list()
        for list_iter in parameter_abb_list:
            for abbrvs in list_iter:
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
        print(f"Parameters {not_available_parameters} cannot be plotted in the Station model")
        # if len(not_available_parameters) > 0:
        #     user_parameter = input(f"parameter abbreviations {not_available_parameters} "
        #                            f"are not recognized to plot data, Please select the "
        #                            f"parameter from {parameter_keys} to add an abbreviation:\t")
        #     if user_parameter in parameter_keys:
        #         user_added_abbreviation = input('Enter abbreviation for the selected parameter:\t')
        #         parameter_abbreviations[user_parameter].append(user_added_abbreviation)
        #     else:
        #         print(f"Parameters {not_available_parameters} cannot be plotted in the Station model")
        return data_to_plot

    @staticmethod
    def plot_station_model(data: dict, plot_dictionary: dict):
        """

        :param plot_dictionary: A dictionary containing Plotting parameters and their respective polt functions
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

        for key, value in data.items():
            if key in plot_dictionary:
                eval(plot_dictionary[key])

        name = 'Station_model.jpeg'
        path = os.path.abspath('Station_model.jpeg')
        plt.axis('off')
        plt.savefig(path, dpi=100)

        return path

    @staticmethod
    def get_time_stamp(time_stamp_string):
        """

        :param time_stamp_string: accepts String in the format --> 'YYYY-MM-DD HH:MM'
        :return: time_stamp object
        """
        """get_time_stamp method  """
        if len(time_stamp_string) == 16:
            ts = dt.strptime(time_stamp_string, '%Y-%m-%d %H:%M')
            return ts
        else:
            ts = dt.strptime(time_stamp_string, '%Y-%m-%d %H:%M:%S')
            return ts

    @staticmethod
    def get_abbreviations_from_file(dictionaries):

        for dictionary in dictionaries:
            if 'station_id' in dictionary:
                if isinstance(dictionary['station_id'], list):
                    parameter_abbreviations = dictionary
        return parameter_abbreviations

    @staticmethod
    def get_meteo_codes_from_file(dictionaries):
        for dictionary in dictionaries:
            if 1 in dictionary:
                meteostat_weather_codes = dictionary
        return meteostat_weather_codes

    @staticmethod
    def get_plotting_dictionary(dictionaries):
        for dictionary in dictionaries:
            if 'station_id' in dictionary:
                if isinstance(dictionary['station_id'], str):
                    plot_dictionary = dictionary
        return plot_dictionary

    def _get_pressure_change_and_difference(p_curr, p_prev):

        pressure_diff = p_curr - p_prev
        if pressure_diff > 0:
            return '-', pressure_diff
        elif pressure_diff < 0:
            return '+', pressure_diff
        return '±', pressure_diff
    @staticmethod
    def get_previous_pressure_values(time_stamp_row_index: list, fetched_data_columns, abbreviations: dict,
                                     fetched_data):
        previous_pressure_values = list()
        for iter1 in abbreviations['pressure']:
            if iter1 in fetched_data_columns:
                val_range = 3
                temp_var = time_stamp_row_index[0] - val_range
                if temp_var >= 0:
                    previous_pressure_values = fetched_data.loc[temp_var:time_stamp_row_index[0], iter1]
                    previous_pressure_values = previous_pressure_values.tolist()
                    previous_pressure_values = [int(iter1) for iter1 in previous_pressure_values]
                else:
                    break
        return previous_pressure_values

    @staticmethod
    def validate_pressure_values_to_plot(pressure_values: list):
        """

        :param pressure_values: A list of Pressure values since last 3 hours
        :return: pressure_change_symbol: str, pressure_diff: int, pressure_tend: int
        """
        if len(pressure_values) == 4:
            current_pressure = pressure_values[3]
            pressure_1hr_ago = pressure_values[2]
            pressure_2hr_ago = pressure_values[1]
            pressure_3hr_ago = pressure_values[0]
            pressure_change_symbol, pressure_diff = StationModelPlot._get_pressure_change_and_difference(current_pressure, pressure_3hr_ago)
            if current_pressure >= pressure_3hr_ago and (pressure_2hr_ago - pressure_3hr_ago >= 3 and pressure_1hr_ago - pressure_2hr_ago >= 3):
                pressure_tend = 0
            elif current_pressure - pressure_3hr_ago >= 1 and (current_pressure - pressure_1hr_ago < 3 and pressure_1hr_ago - pressure_2hr_ago < 3):
                pressure_tend = 1
            elif (current_pressure - pressure_3hr_ago > 3 and (current_pressure - pressure_1hr_ago > 3 and pressure_1hr_ago - pressure_2hr_ago > 3)) or pressure_3hr_ago < pressure_2hr_ago < pressure_1hr_ago < current_pressure:
                pressure_tend = 2
            elif current_pressure - pressure_3hr_ago > 1 and (current_pressure - pressure_1hr_ago >= 3 and pressure_2hr_ago - pressure_1hr_ago >= 3):
                pressure_tend = 3
            elif (pressure_3hr_ago == pressure_2hr_ago == pressure_1hr_ago == current_pressure) or abs(current_pressure - pressure_3hr_ago) <= 1:
                pressure_tend = 4
            elif current_pressure <= pressure_3hr_ago and (pressure_3hr_ago - pressure_2hr_ago >= 3 and pressure_2hr_ago - pressure_1hr_ago >= 3):
                pressure_tend = 5
            elif pressure_3hr_ago - current_pressure > 1 and (current_pressure - pressure_1hr_ago <= 1 and pressure_1hr_ago - pressure_2hr_ago <= 1):
                pressure_tend = 6
            elif (pressure_3hr_ago - current_pressure > 3 and (pressure_1hr_ago - current_pressure >= 3 and pressure_2hr_ago - pressure_1hr_ago >= 3 and pressure_3hr_ago - pressure_2hr_ago >= 3)) or pressure_3hr_ago > pressure_2hr_ago > pressure_1hr_ago > current_pressure:
                pressure_tend = 7
            elif pressure_3hr_ago - current_pressure > 1 and (pressure_1hr_ago - current_pressure >= 3 and pressure_2hr_ago - pressure_1hr_ago >= 3):
                pressure_tend = 8

            return pressure_change_symbol, abs(pressure_diff), pressure_tend
        else:
            return pressure_change_symbol, abs(pressure_diff)

    @staticmethod
    def get_pressure_values_to_plot(pressure_values_to_plot, plot_data: dict):
        if len(pressure_values_to_plot) == 3:
            if pressure_values_to_plot[0] != '':
                plot_data['pressure_change'] = pressure_values_to_plot[0]
            if pressure_values_to_plot[1] != None:
                plot_data['pressure_difference'] = pressure_values_to_plot[1]
            if pressure_values_to_plot[2] >= 0:
                plot_data['pressure_tendency'] = pressure_values_to_plot[2]
                print(plot_data['pressure_tendency'])
        elif len(pressure_values_to_plot) == 2:
            if pressure_values_to_plot[0] != '':
                plot_data['pressure_change'] = pressure_values_to_plot[0]
            if pressure_values_to_plot[1] != None:
                plot_data['pressure_difference'] = pressure_values_to_plot[1]
        return plot_data

    @staticmethod
    def meteostat_weather_codes_conversion(plot_data: dict, st_id: str, data_source_input, meteostat_weather_code_map):
        if data_source_input == 'f':
            plot_data['station_id'] = st_id
            meteo_weather_code = plot_data['present_weather'] if plot_data['present_weather'] >= 0 else 0
            if meteo_weather_code in meteostat_weather_code_map:
                plot_data['present_weather'] = meteostat_weather_code_map[meteo_weather_code]
                plot_data['past_weather'] = meteostat_weather_code_map[meteo_weather_code]
                if plot_data['present_weather'] == 0:
                    warnings.warn(f"The Present Weather and Past Weather "
                                  f"symbols data is inaccurate to plot from Meteostat data")
                return plot_data

    @staticmethod
    def get_input_for_data_source():
        obtain_method = {'fetch_data': 'Enter Valid Station ID to fetch data:\t',
                         'upload_data_file': 'Enter Path to file or File as object:\t'
                         }
        data_source_input = input(
            f'''Enter a method from below: \n {list(obtain_method.keys())[0]}:(f), {list(obtain_method.keys())[1]}(u):\n''')
        if data_source_input.lower() == 'f':
            station_id = input(obtain_method['fetch_data'])
            data_obj = StationModelPlot(station_id=station_id)
            st_time = StationModelPlot.get_time_stamp(
                input("Enter Start time in format: 'YYYY-MM-DD HH:MM:SS ex. 2022-01-10 00:00:00 --:\n"))
            ed_time = StationModelPlot.get_time_stamp(
                input("Enter End time in format: 'YYYY-MM-DD HH:MM:SS ex. 2022-02-20 00:00:00 --:\n"))
            freq = input("Enter observation Frequency from list [Hourly, Daily] : \t")
            fetched_data, fetched_data_columns = data_obj.fetch_station_data(start_time=st_time,
                                                                             end_time=ed_time,
                                                                             obs_frequency=freq)
            fetched_data = fetched_data.fillna('')
            return fetched_data, fetched_data_columns, data_source_input, station_id
        elif data_source_input.lower() == 'u':
            pt_to_file = input(obtain_method['upload_data_file'])
            data_obj = StationModelPlot(path_to_file=pt_to_file)
            fetched_data, fetched_data_columns = data_obj.custom_file_read()
            fetched_data = fetched_data.fillna('')
        return fetched_data, fetched_data_columns, data_source_input

    @staticmethod
    def get_time_stamp_data(abbreviations: dict, fetched_data, fetched_data_columns: list):
        for iter1 in abbreviations['date_time']:
            timestamp_column = iter1
            if timestamp_column in fetched_data_columns:
                timestamp_column_values = fetched_data[timestamp_column]
                time_stamp = StationModelPlot.get_time_stamp(input(
                    f'Enter Time Stamp from {timestamp_column_values} in the format: "YYYY-MM-DD HH:MM:SS ex. 2022-01-10 00:00:00 --: \n'))
                if len(timestamp_column_values) > 0 and isinstance(timestamp_column_values[0], str):
                    time_stamp_data = fetched_data.loc[timestamp_column_values == str(time_stamp)]
                    time_stamp_row_index = fetched_data.index[timestamp_column_values == str(time_stamp)].to_list()
                elif len(timestamp_column_values) > 0:
                    time_stamp_data = fetched_data.loc[timestamp_column_values == time_stamp]
                    time_stamp_row_index = fetched_data.index[timestamp_column_values == time_stamp].to_list()
                time_stamp_data = time_stamp_data.squeeze()
                time_stamp_data = time_stamp_data.fillna('')
        return time_stamp_data, time_stamp_row_index

    @staticmethod
    def get_previous_weather_value(time_stamp_row_index: list, fetched_data_columns, abbreviations: dict, fetched_data,plot_data):
        for iter1 in abbreviations['present_weather']:
            if iter1 in fetched_data_columns:
                if len(time_stamp_row_index) > 0 and (time_stamp_row_index[0] - 3) >= 0:
                    previous_weather = fetched_data[iter1][time_stamp_row_index[0] - 3]
                    plot_data['past_weather'] = previous_weather
                else:
                    previous_weather = 0
                    plot_data['past_weather'] = previous_weather
        return plot_data

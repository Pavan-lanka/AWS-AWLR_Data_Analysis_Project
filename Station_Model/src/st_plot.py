import warnings
from metpy import io
from metpy.plots import StationPlot
from metpy.plots.wx_symbols import current_weather
from metpy.plots.wx_symbols import sky_cover, pressure_tendency
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import meteostat as mt
from datetime import datetime as dt
from dataclasses import dataclass
import metpy
import cv2
import os
import pickle
from pandas_ods_reader import read_ods


@dataclass
class StationModelPlot:
    station_id: str = None
    path_to_file: str = None

    '''
    StationModelPlot Class accepts 
    Station_ID as String. ex:'12992' & 
    path_to_file as Path to file or file as object 
                ex. "/PycharmProjects/AWS-AWLR_Data_Analysis_Project/Station_Model/data/test/example_metar.txt"
    '''

    def fetch_station_data(self, start_time, end_time, obs_frequency='hourly'):
        """
        Args:
            start_time(str): Start time to fetch data Ex: 2023-05-29 07:51:00
            end_time(str): End time to fetch data Ex: 2023-03-29 07:51:00
            obs_frequency(str): observation Frequency of data Ex. (Hourly, Daily)

        Returns:Tuple of (DataFrame, List)
                 containing DataFrame of weather data and columns values of the data as list
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

        Returns:Tuple of (DataFrame, List)
                 containing DataFrame of weather data and columns values of the data as list
        """
        supported_types = ['nc', 'xml', 'txt', 'csv']
        extension_read = {'nc': xr.open_dataset,
                          'xml': pd.read_xml,
                          'txt': io.parse_metar_file,
                          'csv': pd.read_csv
                          }
        extension = self.path_to_file[self.path_to_file.rfind('.'):][1:]
        if extension not in supported_types:
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
                :param parameter_abbreviations:
        :param time_stamp_data:
        :param data_columns:
        :return:
        Args:
            time_stamp_data(dict()): A dictionary of weather parameters, values for weather data
            data_columns(list()): A list of Weather Parameter Abbreviations
            parameter_abbreviations(dict()): A dictionary containing parameter abbreviations

        Returns(dict()):
                        Dictionary of valid Parameter names, values to plot

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
        return data_to_plot

    @staticmethod
    def plot_station_model(data: dict, plot_dictionary: dict):
        """
        Args:
            data(dict): A dictionary containing data to plot into Station Model
            plot_dictionary(dict): A dictionary containing Plotting parameters and their respective polt functions

        Returns(dict):
                Path to Image containing Station Model

        """
        fig, ax = plt.subplots(figsize=(10, 10))
        sp = StationPlot(ax, 0, 0, fontsize=18, spacing=25)
        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        ax.set_title('Station Model', fontsize=22, bbox=dict(boxstyle='square', facecolor='white', alpha=0.3),
                     weight='heavy', family='monospace')
        station_square = plt.Rectangle((-6, -6), 12, 12, fc='white', ec="k")
        # ax.set_aspect()
        ax.add_patch(station_square)
        logo_2 = "April_logo.png"
        logo_1 = "Azista_logo.png"
        cwd = os.getcwd()
        path1 = cwd + "/data/" + logo_1
        path2 = cwd + "/data/" + logo_2
        az_logo = plt.imread(path1)
        ap_logo = plt.imread(path2)
        extent1 = [-8, -5.5, 6.5, 8]
        extent2 = [5, 8, 6, 8]
        plt.imshow(az_logo, extent=extent1, aspect='equal')
        plt.imshow(ap_logo, extent=extent2, aspect='equal')

        for key, value in data.items():
            if key in plot_dictionary:
                eval(plot_dictionary[key])

        name = 'Station_model.jpeg'
        cwd = os.getcwd()
        file_path = cwd + '/data/'
        plt.axis('off')
        plt.savefig(file_path+name, dpi=100)

        return file_path+name

    @staticmethod
    def get_time_stamp(time_stamp_string):
        """
        Args:
            time_stamp_string(str): accepts String in the format --> 'YYYY-MM-DD HH:MM'

        Returns(object):
                        object with time_stamp value

        """
        if len(time_stamp_string) == 16:
            ts = dt.strptime(time_stamp_string, '%Y-%m-%d %H:%M')
            return ts
        else:
            ts = dt.strptime(time_stamp_string, '%Y-%m-%d %H:%M:%S')
            return ts

    @staticmethod
    def get_abbreviations(data: dict):
        """

        Args:
            data(dict): Nested Dictionary containing Multiple dictionaries

        Returns(dict):
                A Dictionary of Abbreviations used to validate parameters

        """
        for iter1 in data:
            if 'station_id' in iter1:
                if isinstance(iter1['station_id'], list):
                    parameter_abbreviations = iter1
        return parameter_abbreviations

    @staticmethod
    def get_meteo_codes_from_file(data):
        """

        Args:
            data(dict): Nested Dictionary containing Multiple dictionaries

        Returns(dict):
                A Dictionary of Integers as keys and values used to validate weather codes

        """
        for iter1 in data:
            if 1 in iter1:
                meteostat_weather_codes = iter1
        return meteostat_weather_codes

    @staticmethod
    def get_plotting_dictionary(data):
        """
        Args:
            data(dict): Nested Dictionary containing Multiple dictionaries

        Returns(dict):
                A Dictionary of weather parameters as keys and their respective plotting function

        """
        for iter1 in data:
            if 'station_id' in iter1:
                if isinstance(iter1['station_id'], str):
                    plot_dictionary = iter1
        return plot_dictionary

    @staticmethod
    def _get_pressure_change(p_curr, p_prev):
        """

        Args:
            p_curr(integer): Current Pressure Value
            p_prev(integer): Previous Pressure Value

        Returns(str):
                    A string containing a special Character to plot Pressure Change

        """
        p_diff = p_curr - p_prev
        if p_diff > 0:
            return '+'
        elif p_diff < 0:
            return '-'
        return '±'

    @staticmethod
    def get_pressure_difference(p_curr, p_prev):
        """

        Args:
            p_curr(integer): Current Pressure Value
            p_prev(integer): Previous Pressure Value

        Returns(integer):
                        An Integer of pressure difference
        """
        p_diff = p_curr - p_prev
        return p_diff

    @staticmethod
    def get_previous_pressure_values(time_stamp_row_index: list, fetched_data_columns, abbreviations: dict,
                                     fetched_data):
        """

        Args:
            time_stamp_row_index(list): A list containing Index value of Time Stamp
            fetched_data_columns(list): A list Containing Column Values of the DataFrame
            abbreviations(list): A Dictionary containing Key to validate Abbreviation
            fetched_data(DataFrame): A DataFrame containing Weather Values

        Returns(list):
                A list containing Previous Pressure Values

        """
        previous_pressure_values = list()
        for iter1 in abbreviations['pressure']:
            if iter1 in fetched_data_columns:
                val_range = 3
                temp_var = time_stamp_row_index[0] - val_range
                if temp_var >= 0:
                    previous_pressure_values = fetched_data.loc[temp_var:time_stamp_row_index[0], iter1]
                    previous_pressure_values = previous_pressure_values.tolist()
                    previous_pressure_values = [int(iter2) for iter2 in previous_pressure_values]
                else:
                    break
        return previous_pressure_values

    @staticmethod
    def validate_pressure_values_to_plot(pressure_values: list):
        """
        Args:
            pressure_values(list): A list containing Previous Pressure Values

        Returns(tuple): A tuple containing validated Pressure values(pressure_change_symbol, pressure_diff,
        pressure_tendency)

        """
        if len(pressure_values) == 4:
            current_pressure = pressure_values[3]
            pressure_1hr_ago = pressure_values[2]
            pressure_2hr_ago = pressure_values[1]
            pressure_3hr_ago = pressure_values[0]
            pressure_change_symbol = StationModelPlot._get_pressure_change(
                current_pressure, pressure_3hr_ago)
            pressure_diff = StationModelPlot.get_pressure_difference(
                current_pressure, pressure_3hr_ago)
            if current_pressure >= pressure_3hr_ago and (
                    pressure_2hr_ago - pressure_3hr_ago >= 3 and pressure_1hr_ago - pressure_2hr_ago >= 3):
                pressure_tend = 0
            elif current_pressure - pressure_3hr_ago >= 1 and (
                    current_pressure - pressure_1hr_ago < 3 and pressure_1hr_ago - pressure_2hr_ago < 3):
                pressure_tend = 1
            elif (current_pressure - pressure_3hr_ago > 3 and (
                    current_pressure - pressure_1hr_ago > 3 and pressure_1hr_ago - pressure_2hr_ago > 3)) or pressure_3hr_ago < pressure_2hr_ago < pressure_1hr_ago < current_pressure:
                pressure_tend = 2
            elif current_pressure - pressure_3hr_ago > 1 and (
                    current_pressure - pressure_1hr_ago >= 3 and pressure_2hr_ago - pressure_1hr_ago >= 3):
                pressure_tend = 3
            elif (pressure_3hr_ago == pressure_2hr_ago == pressure_1hr_ago == current_pressure) or abs(
                    current_pressure - pressure_3hr_ago) <= 1:
                pressure_tend = 4
            elif current_pressure <= pressure_3hr_ago and (
                    pressure_3hr_ago - pressure_2hr_ago >= 3 and pressure_2hr_ago - pressure_1hr_ago >= 3):
                pressure_tend = 5
            elif pressure_3hr_ago - current_pressure > 1 and (
                    current_pressure - pressure_1hr_ago <= 1 and pressure_1hr_ago - pressure_2hr_ago <= 1):
                pressure_tend = 6
            elif (pressure_3hr_ago - current_pressure > 3 and (
                    pressure_1hr_ago - current_pressure >= 3 and pressure_2hr_ago - pressure_1hr_ago >= 3 and pressure_3hr_ago - pressure_2hr_ago >= 3)) or pressure_3hr_ago > pressure_2hr_ago > pressure_1hr_ago > current_pressure:
                pressure_tend = 7
            elif pressure_3hr_ago - current_pressure > 1 and (
                    pressure_1hr_ago - current_pressure >= 3 and pressure_2hr_ago - pressure_1hr_ago >= 3):
                pressure_tend = 8
            else:
                pressure_tend = 4
                warnings.warn('Pressure Tendency Value is Incorrect due to insufficient data')

            return pressure_change_symbol, abs(pressure_diff), pressure_tend

    @staticmethod
    def get_pressure_values_to_plot(pressure_values_to_plot, plot_data: dict):
        """

        Args:
            pressure_values_to_plot(Tuple): A tuple containing Validated Pressure Values to plot
            plot_data(dict): A Dictionary of validated Weather Parameters and their respective Values

        Returns(dict):
                    An Updated Dictionary to plot data with Pressure Parameters, namely(Pressure_Change, Pressure Difference, Pressure_tendency)
                    and their Values

        """
        if len(pressure_values_to_plot) == 3:
            if pressure_values_to_plot[0] != '':
                plot_data['pressure_change'] = pressure_values_to_plot[0]
            if pressure_values_to_plot[1] is not None:
                plot_data['pressure_difference'] = pressure_values_to_plot[1]
            if pressure_values_to_plot[2] >= 0:
                plot_data['pressure_tendency'] = pressure_values_to_plot[2]
        elif len(pressure_values_to_plot) == 2:
            plot_data['pressure_change'] = pressure_values_to_plot[0]
            plot_data['pressure_difference'] = pressure_values_to_plot[1]
        return plot_data

    @staticmethod
    def meteostat_weather_codes_conversion(station_id, plot_data: dict, meteostat_weather_code_map):
        """
        Args:
            station_id(str): A string of Station_id
            plot_data(dict): A Dictionary of validated Weather Parameters and their respective Values
            meteostat_weather_code_map(dict): A Dictionary Containing Weather Code Conversion Map for Meteostat Weather codes

        Returns(dict):
                    An Updated Dictionary to plot data with Pressure Parameters, namely(Pressure_Change, Pressure Difference, Pressure_tendency)
         and their Values

        """
        plot_data['station_id'] = station_id
        if 'present_weather' in plot_data:
            meteo_weather_code = plot_data['present_weather'] if plot_data['present_weather'] >= 0 else 0
            if meteo_weather_code in meteostat_weather_code_map:
                plot_data['present_weather'] = meteostat_weather_code_map[meteo_weather_code]
                plot_data['past_weather'] = meteostat_weather_code_map[meteo_weather_code]
                if plot_data['present_weather'] == 0 or plot_data['past_weather'] == 0:
                    warnings.warn(f"The Present Weather and Past Weather "
                                  f"symbols data is inaccurate to plot from Meteostat data")
                    return plot_data
        else:
            return plot_data

    @staticmethod
    def get_input_for_data_source():
        """

        Returns(tuple):
                A Data Frame of Weather Data, A list of Columns of the DataFrame, The User Selected Method for Data source,
                Station_ID as a String

        """
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
            freq = input("Enter observation Frequency from list [hourly, daily] : \t")
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
        """

        Args:
            abbreviations(dict): A Dictionary containing Key to validate Abbreviation
            fetched_data(DataFrame): A DataFrame containing Weather Values
            fetched_data_columns(list): A list Containing Column Values of the DataFrame

        Returns(tuple):
                A tuple containing Dictionary of plotting data and a list of Index Value

        """
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
    def get_previous_weather_value(time_stamp_row_index: list, fetched_data_columns, abbreviations: dict, fetched_data,
                                   plot_data):
        """
        Args:
            time_stamp_row_index(list): A list containing Index value of Time Stamp
            fetched_data_columns(list): A list Containing Column Values of the DataFrame
            abbreviations(dict): A Dictionary containing Key to validate Abbreviation
            fetched_data(DataFrame): A DataFrame containing Weather Values
            plot_data(dict): A Dictionary of validated Weather Parameters and their respective Values

        Returns(dict):
                An Updated Dictionary of plot data with Pressure Parameters, namely(Pressure_Change, Pressure Difference, Pressure_tendency)
                and their Values

        """
        for iter1 in abbreviations['present_weather']:
            if iter1 in fetched_data_columns:
                if len(time_stamp_row_index) > 0 and (time_stamp_row_index[0] - 3) >= 0:
                    previous_weather = fetched_data[iter1][time_stamp_row_index[0] - 3]
                    plot_data['past_weather'] = previous_weather
                else:
                    previous_weather = 0
                    plot_data['past_weather'] = previous_weather
        return plot_data

    @staticmethod
    def get_station_names(station_id):
        """

        Args(str):
            station_id: A string of Station ID

        Returns(str):
                    A String with updated Station ID

        """
        cwd = os.getcwd()
        file_path = '/data/test/station_ids.ods'
        df = read_ods(cwd+file_path, 1, columns=["Region", "station_name", "st_identifier"])
        if len(station_id) > 0:
            for val in df['st_identifier']:
                if val == station_id:
                    st_name = df.loc[df['st_identifier'] == val]['station_name']
                    st_name = st_name.tolist()
                    station_id = str(station_id + '[' + str(st_name[0]) + ']')
                    return station_id
        else:
            return station_id

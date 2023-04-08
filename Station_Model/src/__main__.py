import warnings
import os
from st_plot import StationModelPlot as sm
import cv2
import pickle


file_path = os.path.abspath('my_dicts.pkl')
with open(file_path, 'rb') as f:
    dictionaries = pickle.load(f)


def main():
    abbrv_for_validation = dict()
    parameter_abbreviations = sm.get_abbreviations_from_file(dictionaries)
    plot_dictionary = sm.get_plotting_dictionary(dictionaries)
    meteo_weather_codes = sm.get_meteo_codes_from_file(dictionaries)
    abbrv_for_validation['date_time'] = parameter_abbreviations['date_time']
    abbrv_for_validation['pressure'] = parameter_abbreviations['pressure']
    abbrv_for_validation['present_weather'] = parameter_abbreviations['present_weather']
    usr_input = sm.get_input_for_data_source()
    if len(usr_input) > 3:
        fetched_data = usr_input[0]
        fetched_data_columns = usr_input[1]
        data_source_input = usr_input[2]
        station_id = usr_input[3]
    else:
        fetched_data = usr_input[0]
        fetched_data_columns = usr_input[1]
        data_source_input = usr_input[2]
    time_stamp_data, time_stamp_row_index = sm.get_time_stamp_data(abbrv_for_validation, fetched_data, fetched_data_columns)
    plot_data = sm.parameter_validation(time_stamp_data, fetched_data_columns, parameter_abbreviations)
    previous_pressure_values = sm.get_previous_pressure_values(time_stamp_row_index, fetched_data_columns, abbrv_for_validation)
    pressure_values_to_plot = sm.get_pressure_values_to_plot(previous_pressure_values)
    plot_data = sm.validate_pressure_values_to_plot(pressure_values_to_plot, plot_data)
    plot_data['past_weather'] = sm.get_previous_weather_value(time_stamp_row_index, fetched_data_columns, abbrv_for_validation)
    if data_source_input == 'f':
        plot_data = sm.meteostat_weather_codes_conversion(plot_data, station_id, data_source_input, meteo_weather_codes)
    path = sm.plot_station_model(plot_data, plot_dictionary)
    return path


if __name__ == '__main__':
    path_to_model = main()
    cv2.waitKey(10)
    img = cv2.imread(path_to_model)
    cv2.imshow('Station Model', img)
    key = cv2.waitKey(0)

    if key > -1 & 0xFF:
        cv2.destroyAllWindows()

import warnings
import os
from st_plot import StationModelPlot as sm
import cv2
import pickle


def main():
    valid_params = dict()
    param_abbrvs = sm.get_abbreviations(archived_data)
    plt_data = sm.get_plotting_dictionary(archived_data)
    meteo_weather_codes = sm.get_meteo_codes_from_file(archived_data)
    valid_params['date_time'] = param_abbrvs['date_time']
    valid_params['pressure'] = param_abbrvs['pressure']
    valid_params['present_weather'] = param_abbrvs['present_weather']
    while True:
        try:
            usr_input = sm.get_input_for_data_source()
            if len(usr_input) > 3:
                fetched_data = usr_input[0]
                fetched_data_cols = usr_input[1]
                data_src_inp = usr_input[2]
                station_id = usr_input[3]
            else:
                fetched_data = usr_input[0]
                fetched_data_cols = usr_input[1]
                data_src_inp = usr_input[2]
            timestamp_data, row_index = sm.get_time_stamp_data(valid_params, fetched_data, fetched_data_cols)
            break
        except Exception as e:
            print(e)
            continue
    plot_data = sm.parameter_validation(timestamp_data, fetched_data_cols, param_abbrvs)
    print(plot_data)
    past_pres_vals = sm.get_previous_pressure_values(row_index, fetched_data_cols, valid_params, fetched_data)
    print(past_pres_vals)
    pres_vals_to_plot = sm.validate_pressure_values_to_plot(past_pres_vals)
    plot_data = sm.get_pressure_values_to_plot(pres_vals_to_plot, plot_data)
    plot_data = sm.get_previous_weather_value(row_index, fetched_data_cols, valid_params, fetched_data, plot_data)
    if data_src_inp == 'f':
        plot_data = sm.meteostat_weather_codes_conversion(station_id, plot_data, meteo_weather_codes)
    elif 'station_id' in plot_data:
        station_id = plot_data['station_id']
        plot_data['station_id'] = sm.get_station_names(station_id)
        print(plot_data['station_id'])
    path = sm.plot_station_model(plot_data, plt_data)
    return path


if __name__ == '__main__':
    cwd = os.getcwd()
    file_path = '/data/my_dicts.pkl'
    with open(cwd+file_path, 'rb') as f:
        archived_data = pickle.load(f)
    path_to_model = main()
    cv2.waitKey(5)
    img = cv2.imread(path_to_model)
    cv2.imshow('Station Model', img)
    key = cv2.waitKey(0)

    if key > -1 & 0xFF:
        cv2.destroyAllWindows()

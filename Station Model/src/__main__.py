from st_plot import StationModelPlot
import cv2


def main():
    obtain_method = {'fetch_data': 'Enter Valid Station ID to fetch data:\t',
                     'upload_data_file': 'Enter Path to file or File as object:\t'
                     }
    abbreviations = {
        'date_time': ['valid', 'time', 'date_time', 'time1', 'time_stamp', 'DATE_TIME'],
        'pressure': ['PRESSURE', 'pres', 'mslp', 'atmospheric_pressure', 'air_pressure_at_sea_level'],
        'present_weather': ['coco', 'current_weather', 'wxcodes', 'current_wx1', 'current_wx1_symbol',
                            'present_weather']
    }
    while True:
        ip = input(
            f'''Enter a method from below: \n {list(obtain_method.keys())[0]}:(f), {list(obtain_method.keys())[1]}(u):\n''')
        if ip.lower() == 'f':
            st_id = input(obtain_method['fetch_data'])
            st = StationModelPlot(station_id=st_id)
            st_time = StationModelPlot.get_time_stamp(
                input("Enter End time in format: 'YYYY-MM-DD HH:MM:SS ex. 2022-01-10 00:00:00 --:\n"))
            ed_time = StationModelPlot.get_time_stamp(
                input("Enter End time in format: 'YYYY-MM-DD HH:MM:SS ex. 2022-01-20 00:00:00 --:\n"))
            freq = input("Enter observation Frequency from list [Hourly, Daily] : \t")
            try:
                fetched_data, fetched_data_columns = st.fetch_station_data(start_time=st_time, end_time=ed_time,
                                                                           obs_frequency=freq)
                fetched_data = fetched_data.fillna('')
            except Exception as e:
                print('Please Enter Valid Station ID , Valid Start time and End time in format: YYYY-MM-DD HH:MM:SS')
                continue
            pass
        elif ip.lower() == 'u':
            pt_to_file = input(obtain_method['upload_data_file'])
            try:
                st = StationModelPlot(path_to_file=pt_to_file)
                fetched_data, fetched_data_columns = st.custom_file_read()
                fetched_data = fetched_data.fillna('')
            except Exception as e:
                print('Entered Path File is Incorrect please enter a valid file path, or file as an object')
                continue
            pass
        else:
            continue
        while True:
            try:
                for iteration2 in range(len(abbreviations['date_time'])):
                    ts_column = abbreviations['date_time'][iteration2]
                    if ts_column in fetched_data_columns:
                        ts_column_values = fetched_data[ts_column]
                        time_stamp = StationModelPlot.get_time_stamp(input(
                            f'Enter Time Stamp from {ts_column_values} in the format: "YYYY-MM-DD HH:MM:SS ex. 2022-01-10 00:00:00 --: \n'))
                        if len(ts_column_values) > 0 and isinstance(ts_column_values[0], str):
                            ts_data = fetched_data.loc[ts_column_values == str(time_stamp)]
                            idx = fetched_data.index[ts_column_values == str(time_stamp)].to_list()
                        elif len(ts_column_values) > 0:
                            ts_data = fetched_data.loc[ts_column_values == time_stamp]
                            idx = fetched_data.index[ts_column_values == time_stamp].to_list()
                        ts_data = ts_data.squeeze()
                        ts_data = ts_data.fillna('')
                        break
                pres_value_dict = dict()
                weather_3hrs_ago = None
                for iteration in abbreviations['pressure']:
                    if iteration not in fetched_data_columns:
                        pass
                    elif iteration in fetched_data_columns:
                        loop = 3
                        while loop > 0:
                            if len(idx) > 0 and (idx[0] - loop) >= 0:
                                pres_value_dict[loop] = int(fetched_data[iteration][idx[0] - loop])
                                loop -= 1
                            else:
                                break
                        pass
                for iteration1 in abbreviations['present_weather']:
                    if iteration1 not in fetched_data_columns:
                        pass
                    elif iteration1 in fetched_data_columns:
                        if len(idx) > 0 and (idx[0] - 3) >= 0:
                            weather_3hrs_ago = fetched_data[iteration1][idx[0] - 3]
                        else:
                            weather_3hrs_ago = 0
                            pass

                pass
            except Exception as e:
                print(e)
                continue
            #/home/hp/PycharmProjects/AWS-AWLR_Data_Analysis_Project/Station Model/data/test/weather_data.csv
            plot_data = StationModelPlot.parameter_validation(ts_data, fetched_data_columns)
            pres_value_dict[0] = int(plot_data['pressure'])
            print(pres_value_dict)
            pres_values = StationModelPlot.press_values(pres_value_dict)
            if len(pres_values) == 3:
                if pres_values[0] != '':
                    plot_data['pressure_change'] = pres_values[0]
                if pres_values[1] != None:
                    plot_data['pressure_difference'] = pres_values[1]
                if pres_values[2] >= 0:
                    plot_data['pressure_tendency'] = pres_values[2]
            elif len(pres_values) == 2:
                if pres_values[0] != '':
                    plot_data['pressure_change'] = pres_values[0]
                if pres_values[1] != None:
                    plot_data['pressure_difference'] = pres_values[1]
            plot_data['past_weather'] = weather_3hrs_ago
            if ip == 'f':
                plot_data['station_id'] = st_id
            path = StationModelPlot.plot_station_model(data=plot_data)

            break
        break
    return path


if __name__ == '__main__':
    path_to_model = main()
    cv2.waitKey(10)
    img = cv2.imread(path_to_model)
    cv2.imshow('Station Model', img)
    key = cv2.waitKey(0)
    # if k == 27:  # close on ESC key
    #     cv2.destroyAllWindows()
    if key > -1 & 0xFF:
        cv2.destroyAllWindows()
    cv2.destroyAllWindows()
# /home/hp/example_metar.txt
# 2023-04-29 05:51:00
# 2023-04-29 07:08:00
# /home/hp/PycharmProjects/AWS-AWLR_Data_Analysis_Project/Station Model/data/test/weather_data.csv
# 2023-04-05 12:51:00
# 2022-01-10 04:00:00
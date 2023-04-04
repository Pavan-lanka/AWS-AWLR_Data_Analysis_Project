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
                        ts = StationModelPlot.get_time_stamp(input(
                            f'Enter Time Stamp from {ts_column_values} in the format: "YYYY-MM-DD HH:MM:SS ex. 2022-01-10 00:00:00 --: \n'))
                        ts_data = fetched_data.loc[ts_column_values == ts]
                        ts_data = fetched_data.loc[ts_column_values == str(ts)]
                        ts_data = ts_data.squeeze()
                        ts_data = ts_data.fillna('')
                        break
                # pres_value_dict = dict()
                # weather_3hrs_ago = None
                # idx = fetched_data.index[fetched_data['date_time'] == ts].to_list()
                # if idx[0] - 3 >= 3:
                #     print(idx[0])
                # loop = 3
                # while loop > 0:
                #     for iteration in abbreviations['pressure']:
                #         print(iteration)
                #         if iteration in fetched_data_columns:
                #             print(iteration)
                #             if (int(idx[0]) - loop) >= 0:
                #                 pres_value_dict[loop] = fetched_data[iteration][(idx[0] - loop)]
                #                 loop -= 1
                #                 break
                #             else:
                #                 break
                #         else:
                #             break
                #     break
                # for iteration1 in abbreviations['present_weather']:
                #     if iteration1 in fetched_data_columns:
                #         print(iteration1)
                #         if (int(idx[0]) - 3) >= 0:
                #             weather_3hrs_ago = fetched_data[iteration1][idx[0] - 3]
                #             break
                #         else:
                #             break
                #     else:
                #         break

                pass
            except Exception as e:
                print('Enter Time Stamp in valid format: YYYY-MM-DD HH:MM:SS')
                continue
            print(weather_3hrs_ago)
            print(pres_value_dict)
            plot_data = StationModelPlot.parameter_validation(ts_data, fetched_data_columns)
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

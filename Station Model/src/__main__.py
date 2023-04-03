from st_plot import StationModelPlot
import cv2


def main():
    obtain_method = {'fetch_data': 'Enter Valid Station ID to fetch data:\t',
                     'upload_data_file': 'Enter Path to file or File as object:\t'
                     }
    parameter_abb = {
        'date_time': ['valid', 'time', 'date_time', 'time1', 'time_stamp', 'DATE_TIME'],
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
            fetched_data, fetched_data_columns = st.fetch_station_data(start_time=st_time, end_time=ed_time,
                                                                       obs_frequency=freq)
            fetched_data = fetched_data.fillna('')
            pass
        elif ip.lower() == 'u':
            pt_to_file = input(obtain_method['upload_data_file'])
            st = StationModelPlot(path_to_file=pt_to_file)
            fetched_data, fetched_data_columns = st.custom_file_read()
            fetched_data = fetched_data.fillna('')
            pass
        else:
            continue
        date_abbreviations = {'date_time': ['valid', 'time', 'date_time', 'time1', 'time_stamp', 'DATE_TIME']}
        while True:
            for iter in range(len(date_abbreviations['date_time'])):
                idx = date_abbreviations['date_time'][iter]
                if idx in fetched_data_columns:
                    ts_column_name = fetched_data[idx]
                    ts = StationModelPlot.get_time_stamp(input(
                        f'Enter Time Stamp from {ts_column_name} in the format: "YYYY-MM-DD HH:MM:SS ex. 2022-01-10 00:00:00 --: \n'))
                    ts_data = fetched_data.loc[ts_column_name == ts]
                    ts_data = fetched_data.loc[ts_column_name == str(ts)]
                    ts_data = ts_data.squeeze()
                    ts_data = ts_data.fillna('')
                    break
            pass
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
    key = cv2.waitKey(0) & 0xFF
    # if k == 27:  # close on ESC key
    #     cv2.destroyAllWindows()
    if key > -1:
        cv2.destroyAllWindows()
# /home/hp/example_metar.txt
# 2023-04-29 05:51:00
# 2023-04-29 07:08:00
# /home/hp/PycharmProjects/AWS-AWLR_Data_Analysis_Project/Station Model/data/test/weather_data.csv

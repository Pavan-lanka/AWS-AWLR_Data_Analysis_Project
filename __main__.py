# from metpy.io import *
# # import st_plot as st
# import xarray as xr
# import pandas as pd
#
#
# #
# # def __main__():
# #     i = st.FetchData.get_input_date_time()
#
#
# def custom_file_read(path_to_file):
#     supported_types = ['nc', 'xml', 'txt', 'csv']
#     extension_read = {'nc': xr.open_dataset,
#                       'xml': pd.read_xml,
#                       'txt': parse_metar_file,
#                       'csv': pd.read_csv
#                       }
#     extension = path_to_file[path_to_file.rfind('.'):][1:]
#     if extension not in supported_types:
#         raise TypeError(f'Supported file formats are {supported_types}')
#     elif extension == 'nc':
#         data = extension_read['nc'](filename_or_obj=path_to_file, engine="netcdf4")
#         data = data.metpy.parse_cf()
#         data = data.to_dataframe()
#         data = data.reset_index()
#     else:
#         data = extension_read[extension](path_to_file)
#     d_parameters = list(data.columns.values)
#     return data, d_parameters
#
#
# a, b = custom_file_read(r"/home/hp/metar_vij.txt")
# print(b)


from metpy.plots import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class StationModel:
    def __init__(self, sp=None, ax=None):
        self.sp = sp
        self.ax = ax

    def plot_temperature(self, temperature):
        # to plot temperature in station model
        self.sp.plot_text((-4, 3), text=[str(temperature) + '°C'], fontsize=13)

    def plot_dew_point(self, dew_point):
        # to add dew_point to the model
        self.sp.plot_text((-4, 3), text=[str(dew_point) + '°C'], fontsize=13)

    def plot_visibility(self, visibility_distance):
        # to add visibility_distance to the model
        self.sp.plot_text((-6, 0), text=[str(visibility_distance) + 'miles'], fontsize=13)

    def plot_barb(self, wind_speed, wind_direction):
        # to position wind-barb in the center of the model
        # u = -wind_speed * np.sin(np.radians(wind_direction))
        # v = -wspd_mps * math.cos(np.radians(wind_direction))
        self.sp.plot_barb(u=[-wind_speed * np.sin(np.radians(wind_direction))],
                          v=[-wind_speed * np.cos(np.radians(wind_direction))], length=11)

        # to add wind speed in knots at the end of the barb
        self.ax.text(1.5 * np.sin(np.radians(wind_direction)), 1.5 * np.cos(np.radians(wind_direction)),
                     str(wind_speed) + ' kts', ha='center', va='bottom', rotation=0, fontsize=10, alpha=0.3)

    def plot_pressure(self, pressure):
        # to add pressure to the model
        self.sp.plot_text((4, 3), text=[str(pressure) + ' hPa'], fontsize=13)

    def plot_pressure_change(self, press_change):
        # to add pressure_change to the model
        self.sp.plot_text((3.2, 0), text=[str(press_change)], fontsize=13)

    def plot_pressure_difference(self, pressure_difference):
        # to add pressure_difference to the model
        self.sp.plot_text((4, 0), text=[str(pressure_difference)], fontsize=13)

    def plot_sky_cover_at_lowest_cloud(self, sky_cover_at_lowest_cloud):
        # to add sky_cover_of the lowest cloud to the model
        self.sp.plot_text((0, -4), text=[str(sky_cover_at_lowest_cloud)], fontsize=13)

    def plot_cloud_text(self, cloud_height):
        # to add height of the cloud base
        self.sp.plot_text((-2, -5.5), text=[str(cloud_height)], fontsize=13)

    def plot_precipitation(self, precipitation):
        # to add precipitation to the model
        self.sp.plot_text((2, -5.5), text=[str(precipitation)], fontsize=13)

    def plot_sky_cover(self, sky_covered: dict, code):
        # to add Sky_cover symbol to the model
        self.sp.plot_symbol((0, 0), codes=sky_covered[code], symbol_mapper=sky_cover, fontsize=25)

    def plot_pressure_tendency(self, press_tend: dict, code):
        # to add pressure_tendency symbol to the model

        self.sp.plot_symbol((5, 0), codes=press_tend[code], symbol_mapper=pressure_tendency,
                            va='center', ha='center', fontsize=25)

    def plot_low_clouds(self, low_cloud: dict, code):
        # to add low_clouds symbol to the model
        self.sp.plot_symbol((-2, -3.5), codes=low_cloud[code], symbol_mapper=low_clouds,
                            va='center', ha='center', fontsize=25)

    def plot_mid_clouds(self, mid_cloud: dict, code):
        # to add mid_clouds symbol to the model
        self.sp.plot_symbol((2, 3), codes=mid_cloud[code], symbol_mapper=mid_clouds,
                            va='center', ha='center', fontsize=25)

    def plot_high_clouds(self, high_cloud: dict, code):
        # to add high_clouds symbol to the model
        self.sp.plot_symbol((1, 5), codes=high_cloud[code], symbol_mapper=high_clouds,
                            va='center', ha='center', fontsize=25)

    def plot_present_weather(self, present_weather: dict, code):
        # to add present_weather symbol to the model
        self.sp.plot_symbol((-4, 0), codes=present_weather[code], symbol_mapper=current_weather,
                            va='center', ha='center', fontsize=25)

    def plot_past_weather(self, past_weather: dict, code):
        # to add past_weather symbol to the model
        self.sp.plot_symbol((2, -3.5), codes=past_weather[code], symbol_mapper=current_weather,
                            va='center', ha='center', fontsize=25)

    def plot_station_model(self, plot: dict):
        fig, ax = plt.subplots(figsize=(10, 10))
        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
        self.sp = StationPlot(ax, 0, 0, fontsize=13, spacing=25)
        self.ax.set_title('Station Model')
        station_circle = patches.Circle((0, 0), radius=7, lw=1, edgecolor='k', facecolor='w')
        self.ax.add_patch(station_circle)
        plot = [self.plot_past_weather()]
        return plt.show()

# adding metpy logo at the corner
# al = add_metpy_logo(fig=fig, x=8, y=8, zorder=5, size='small')

# plt.grid()

# Define some sample data
# temperature = 15.6
# dewpoint = 10.2
# wind_speed = 200
# wind_direction = 30
# pressure = 1010
# cloud_height = 5
# high_cloud = ''
# mid_cloud = ''
# low_cloud = ''
# sky_covered = ''
# visibility_distance = 0.5
# present_weather = ''
# past_weather = ''
# press_tend = ''
# press_change = '+'
# pressure_difference = 15
# precipitation = '.45'
# sky_cover_at_lowest_cloud = 8

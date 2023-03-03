import metpy.plots as mplt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import config

fig, ax = plt.subplots(figsize=(10, 10))

ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)


ax.set_title('Station Model')


temperature = 15.6
dewpoint = 10.2
wind_speed = int(21 // 1.151)
wind_direction = 30
pressure = 1010
cloud_height = '5'
high_cloud = '*'
mid_cloud = '*'
low_cloud = '*'
sky_cover = 'O'
visibility_distance = '0.5'
present_weather = '*'
past_weather = '*'
pressure_tendency = '/'
pressure_change = '+'
pressure_difference = '15'
precipitation = '.45'
sky_cover_at_lowest_cloud = 8

# Draw the station model
station_circle = patches.Circle((0, 0), radius=7, lw=1, edgecolor='k', facecolor='w')
ax.set_aspect(1)
ax.add_patch(station_circle)

# to plot temperature in the model
ax.text(-4, 4, str(temperature) + '°C', ha='center', va='center', fontsize=13)

# to plot dew_point temperature in the model
ax.text(-4, -4, str(dewpoint) + '°C', ha='center', va='center', fontsize=13)

# to plot visibility distance in the model
ax.text(-4, 0, str(visibility_distance) + 'miles', ha='center', va='center', fontsize=13)

sp = mplt.StationPlot(ax, 0, 0, clip_on=True, fontsize=13)

sp.plot_barb(u=[-wind_speed * np.sin(np.radians(wind_direction))],
             v=[-wind_speed * np.cos(np.radians(wind_direction))], length=12)

ax.text(3 * np.sin(np.radians(wind_direction)), 3 * np.cos(np.radians(wind_direction)),
        str(wind_speed) + ' kts', ha='center', va='center', fontsize=13)
# to add pressure to the model
ax.text(4, 4, str(pressure) + ' hPa', ha='center', va='center', fontsize=13)

# to add pressure_tendency to the model
ax.text(5, 0, str(pressure_tendency), ha='center', va='center', fontsize=13)

# to add pressure_change to the model
ax.text(3,0, str(pressure_change), ha='center', va='center', fontsize=13)

# to add pressure_difference to the model
ax.text(4, 0, str(pressure_difference), ha='center', va='center', fontsize=13)

# to add sky_cover to the model
ax.text(0, 0, str(sky_cover), ha='center', va='center', fontsize=18)

# to add sky_cover_of the lowest cloud to the model
ax.text(0, -4, str(sky_cover_at_lowest_cloud), ha='center', va='center', fontsize=13)

# to add height of the cloud base
ax.text(-2, -4, str(cloud_height), ha='center', va='center', fontsize=13)

# to add precipitation to the model
ax.text(2, -6, str(precipitation), ha='center', va='center', fontsize=13)

# sp.plot_symbol('C', symbol_mapper='50', codes= 5)
plt.grid()
plt.show()

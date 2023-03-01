import metpy.plots.station_plot as sp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines

fig, ax = plt.subplots()

ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)

ax.set_title('Station Model')

# Define some sample data
temperature = 15.6
dewpoint = 10.2
wind_speed = 10
wind_direction = 220
pressure = 1010
altimeter = 30.00
sky_cover_by_lowest_cloud = 6

# Draw the station model
station_circle = patches.Circle((0, 0), radius=7, lw=1, edgecolor='k', facecolor='w')
ax.set_aspect( 1 )
ax.add_patch(station_circle)

ax.text(-4, 2, str(temperature) + '°C', ha='center', va='center', fontsize=8)

ax.text(-4, -2, str(dewpoint) + '°C', ha='center', va='center', fontsize=8)

ax.text(0, -2, str(sky_cover_by_lowest_cloud) + '°C', ha='center', va='center', fontsize=8)


wind_direction_line = lines.Line2D([0, 3.5 * np.sin(np.radians(wind_direction))], [0, 3.5 * np.cos(np.radians(wind_direction))],
                               linewidth=1, color='k')
ax.add_line(wind_direction_line)
ax.text(4 * np.sin(np.radians(wind_direction)), 4 * np.cos(np.radians(wind_direction)),
        str(wind_speed) + ' kts', ha='center', va='center', fontsize=8)

pressure_text = ax.text(4,2, str(pressure) + ' hPa', ha='center', va='center', fontsize=8)

pressure_arrow = patches.FancyArrowPatch((0, -2), (4,0),linewidth=1, color='k', arrowstyle='->', mutation_scale=20)
ax.add_patch(pressure_arrow)


plt.grid()
plt.show()
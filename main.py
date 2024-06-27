from sgp4.api import Satrec, jday
from datetime import datetime, timedelta
import pytz as pytz
import matplotlib.pyplot as plt
import numpy as np


# input_file = input("Enter TLE data file : ")

# constants
MU = 398600.4418  # Earth's standard gravitational parameter (km^3/s^2)
R_EARTH = 6371  # Earth's radius in km (approximate value)

input_file = "data-set.txt"
with open(input_file, 'r') as file:
    lines = file.readlines()
    if len(lines) < 3:
        raise ValueError("The file does not contain enough lines for a TLE set.")

# satellite name
name = lines[0].strip()
# lines with the data
line1 = lines[1].strip()
line2 = lines[2].strip()

satellite = Satrec.twoline2rv(line1, line2)

# time range
start_time = datetime.now(pytz.UTC)
end_time = start_time + timedelta(hours=3)  # 3 hours of orbit
current_time = start_time

times = []
positions = []
interval = timedelta(minutes=1)

# get current UTC date and time
while current_time <= end_time:
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second

    # calculate Julian date and fractional part of the day
    jd, fr = jday(year, month, day, hour, minute, second)

    # compute satellite's position and velocity
    e, r, v = satellite.sgp4(jd, fr)
    if e == 0:
        times.append(current_time)
        positions.append(r)
    else:
        print(f"Error: {e}")

    current_time += interval

positions = np.array(positions)
x = positions[:, 0]
y = positions[:, 1]
z = positions[:, 2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, z, color="red",label=f'{name} Orbit')
ax.scatter(0, 0, 0, color='blue', label='Earth') # representing Earth

a, p = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j] # azimuth and polar angle

# transform spherical coordinates into Cartesian coordinates
earth_x = R_EARTH * np.cos(a) * np.sin(p)
earth_y = R_EARTH * np.sin(a) * np.sin(p)
earth_z = R_EARTH * np.cos(p)
ax.plot_wireframe(earth_x, earth_y, earth_z, color="b", alpha=0.5)

# Labels and title
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.set_title(f'3D Plot of {name} Orbit')
ax.legend()

plt.savefig('satellite_orbit.png')
plt.close()

from sgp4.api import Satrec, jday
from datetime import datetime, timedelta
import pytz
import matplotlib.pyplot as plt
import numpy as np

# Constants
MU = 398600.4418  # Earth's standard gravitational parameter (km^3/s^2)
R_EARTH = 6371  # Earth's radius in km (approximate value)

# Read TLE data from file
input_file = "data-set.txt"
with open(input_file, 'r') as file:
    lines = file.readlines()
    if len(lines) < 3:
        raise ValueError("The file does not contain enough lines for a TLE set.")

# Satellite name
name = lines[0].strip()
# Lines with the TLE data
line1 = lines[1].strip()
line2 = lines[2].strip()

satellite = Satrec.twoline2rv(line1, line2)

# Get TLE epoch year and day of the year
epoch_year = int("20" + line1[18:20])
epoch_day = float(line1[20:32])

# Convert epoch day to datetime
epoch_datetime = datetime(epoch_year, 1, 1) + timedelta(days=epoch_day - 1)
jd_epoch, fr_epoch = jday(epoch_datetime.year, epoch_datetime.month, epoch_datetime.day,
                          epoch_datetime.hour, epoch_datetime.minute, epoch_datetime.second)

# Compute satellite's position and velocity at TLE epoch
e, r, v = satellite.sgp4(jd_epoch, fr_epoch)
if e == 0:
    satellite_pos = r
    print(f"Satellite position at TLE epoch: {satellite_pos}")
else:
    print(f"Error in computing satellite position: {e}")
    satellite_pos = [0, 0, 0]

# Use TLE epoch as start time
start_time = epoch_datetime
end_time = start_time + timedelta(hours=3)  # 3 hours of orbit
current_time = start_time

times = []
positions = []
interval = timedelta(minutes=1)

# Get satellite positions over the time range
while current_time <= end_time:
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute
    second = current_time.second

    # Calculate Julian date and fractional part of the day
    jd, fr = jday(year, month, day, hour, minute, second)

    # Compute satellite's position and velocity
    e, r, v = satellite.sgp4(jd, fr)
    if e == 0:
        times.append(current_time)
        positions.append(r)
    else:
        print(f"Error: {e}")

    current_time += interval

# Retrieve coordinates
positions = np.array(positions)
x = positions[:, 0]
y = positions[:, 1]
z = positions[:, 2]

# Plot 3D representation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot Earth center
ax.scatter(0, 0, 0, color='blue', label='Earth')

# Plot satellite position at TLE epoch
ax.scatter(satellite_pos[0], satellite_pos[1], satellite_pos[2], color='green', label=f"{name} current position")

# Plot the orbit path
ax.plot(x, y, z, color='red', label=f'{name} Orbit')

# Create wireframe for Earth
a, p = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
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

# Print coordinates to verify
print(f"First position in orbit path: {positions[0]}")
print(f"Last position in orbit path: {positions[-1]}")

# Satellite Tracking Program

## Introduction

This python program tracks the position (and orbit!) of a spacecraft relative to Earth, given its TLE data. Using Matplotlib, it will represent, in 3 dimensions, the orbit as well as the position of the spacecraft at epoch relative to Earth. To compute the position and orbit, I used NASA's sgp4 model, integrated as a library.

## Overview

As a kid, I always enjoyed space and space-related stuff (like Star Wars). So I decided to track satellites, because it would let me use my skills in programming for a personnal interest.

## Implementation Details

### Libraries

I used the libraries `sgp4.api` for computing the actual satellite data, `datetime` to compute the orbit over 3 hours, `matplotlib.pyplot` for the graphical representation, as well as `numpy` for convenient mathematical computing (mainly algebra).

Also, this was made in python version 3.11.9.

### Comments

I added comments on the most part of my program, so it should be easy to follow. If you have any questions, don't hesitate to contact me.


## Usage

To use the program, make sure to add a .txt file in the same directory as the file, with correct TLE data. After executing the program, you will be prompted to enter the file path. For the file that I have shared, just type "data-set.txt" and enter. The output will show on another file, "satellite_orbit.png".

For now only one epoch data from one spacecraft can be added, but I might enhance the programs functionalities in the future.

## Conclusion

This is my first "real" python project, that I've pushed on GitHub anyways. While python was basically the first language I started programming in, I never went into the details of the language (not that I have with this project, but I still went deeper than usual). It was a pretty fun challenge to work with TLE data and sgp4 and all these space-related things, given that it was my first real time. Back in high school I wasn't that good in physics class, and I haven't had much interest in space ever since.

I don't know if I'll ever improve the program, but if you want me to, again don't hesitate to contact me!

#### Feel free to adjust or add more content as needed!

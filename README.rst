# FlowTools
FlowTools is a python package designed for the analysis of fluid flow data, including  of turbulent fluid dynamics and wind energy. The main object class in FlowTools is the FlowField class. All other other functions operate on instances of this class. FlowField requires two inputs: (1) velocities - a dict containing instantaneous velocities u, v, w, of a common size, (2) coordinates - a dict containing the coordinates, x, y, z, t, of the data.

## Getting Started
FlowTools does not include an data i/o, and requires that the user load data and format it correctly before constructing a FlowField object. Load data and arrange it into dicts of np.arrays where each array has a common shape.

## Required packages
numpy - used to structure data into arrays, perform basic operations, etc.
matplotlib - used in flow visualization
file i/o - some sort of data importing and exporting utilities. Will depend on the particular data of interest (csv, h5py, etc.)

## Prerequisites
Python 3.6 - working knowledge

## Installing
Download or clone git repo. Go to town.

## Example usage:
```
import numpy as np
import matplotlib.pyplot as plt
import FlowTools as ft

#%% load data and make dictionaries for velocity and coordinates
indat = h5py.File('testdata.csv')

u = np.asarray(indat['u'])
v = np.asarray(indat['v'])
w = np.asarray(indat['w'])
x = np.asarray(indat['x'])
y = np.asarray(indat['y'])
z = np.asarray(indat['z'])
timevec = np.asarray(indat['t'])

velocities = {'u': u,
'v': v,
'w': w}

coordinates = {'x': x,
'y': y,
'z': z,
't': timevec}
# create FlowField object
testflow = ft.FlowField(velocities, coordinates)
# print object attributes
testflow.who()
```


## Version
The current version of the package is v.0.0.

## Authors
Nicholas Hamilton
nicholas.hamilton@nrel.gov

## License
This project is licensed under the Apache License - see the LICENSE file for details

## Acknowledgments
Thanks to anyone who would like to contribute!

## Contributing
Please read CONTRIBUTING for details on our code of conduct, and the process for submitting pull requests to us.

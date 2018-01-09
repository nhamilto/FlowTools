Example usage
==================
FlowTools does not *yet* include an data i/o, and requires that the user load data and format it correctly before constructing a FlowField object. Load data and arrange it into dicts of np.arrays where each array has a common shape.
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

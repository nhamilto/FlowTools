#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 09:27:01 2018

@author: nhamilto
@contact: nicholas.hamilton@nrel.gov
@version: v.0.1
"""

import numpy as np
import matplotlib.pyplot as plt
import h5py 
import sys
sys.path.append('/Users/nhamilto/Documents/FlowTools')

import flowtools as ft
#from flowtools import FlowField

def clall():
    plt.close('all')

def minmax(data):
    minval = np.min(data)
    maxval = np.max(data)
    print('min:', minval)
    print('max:', maxval)
#%% load data and make dictionaries for velocity and coordinates
indat = h5py.File('testdata2.mat')

u = np.asarray(indat['u'])
v = np.asarray(indat['v'])
w = np.asarray(indat['w'])
z = np.asarray(indat['z'])
y = np.asarray(indat['y'])
timevec = np.asarray(indat['t'])

u = u.swapaxes(0,-1)
v = v.swapaxes(0,-1)
w = w.swapaxes(0,-1)

velocities = {'u': u,
              'v': v,
              'w': w}

y, z = np.meshgrid(y, z)

coordinates = {'y': y,
               'z': z,
               't': timevec}

#%%

flowtest = ft.FlowField(velocities, coordinates)
flowtest.mean_flow()
flowtest.turbulent_stresses()
ft.snapshot_POD.decompose(flowtest)
fig = ft.snapshot_POD.check_lam(flowtest)
ft.snapshot_POD.calc_coefficients(flowtest)
fig, ax = ft.snapshot_POD.coeff_plot(flowtest)
ft.snapshot_POD.recompose_rst(flowtest)
        
flowtest.who()

fig, axs = ft.vis.rst_contours(flowtest, ['z', 'y'], flowtest.rst, commonscale = False)
fig, axs = ft.vis.rst_contours(flowtest, ['z', 'y'], flowtest.POD['rst'], commonscale = False)

ft.snapshot_POD.recompose_flucfield(flowtest)
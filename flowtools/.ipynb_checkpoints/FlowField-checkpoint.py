#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 10:44:24 2018

FlowField object creator within the FlowTools package.

@author: nhamilto
@contact: nicholas.hamilton@nrel.gov
@version: v.0.1
"""

import numpy as np
import matplotlib.pyplot as plt

class FlowField:
    """
        The Flowfield class accepts velocities and coordinate information as
        inputs and contains internal methods that produce statistics and 
        descriptive elements of the field (i.e. turbulence, vorticity, etc.)
        
        velocities - dict containing at least one of 'u', 'v', 'w'
                     assumed to be arranged as u = f(x,y,z,t)
        coordinates - dict containing at least one of 'x', 'y', 'z', 't'
        
    """
  
    def __init__(self, velocities, coordinates):
        # velocity components and list
        self.velocities = velocities.copy()        
        # establish size of data shape 
        # named axes for axis-dependent functions
        self.npts = {}
        dummyindex = 0; self.namedaxes = {}
        for key in coordinates:
            self.npts[key] = len(np.unique(coordinates[key]))
            self.namedaxes[key] = dummyindex
            dummyindex += 1
        # separate time from spatial coordinates
        self.coordinates = coordinates.copy()
        self.time = self.coordinates.pop('t')
        # number of coordinates
        self.ncoords = len(coordinates.keys())
        self.ncomps = len(velocities.keys())          
        
        
    #### field properties
    # ensemble averaged velocities over desired axis (usually time)
    def mean_flow(self):
        self.meanfield = {}
        for key in self.velocities:
            self.meanfield[key.upper()] = self.velocities[key].mean(axis = self.namedaxes['t'])
            
    # calculate fluctuations of instatantaneous velocity from ensemble average
    def velocity_flucs(self):
        self.flucfield = {}
        # broadcast subtract mean from instantaneous fields
        for key in self.velocities:
            self.flucfield[key] = self.velocities[key] - \
                self.velocities[key].mean(axis = self.namedaxes['t'])[...,np.newaxis]

    # Reynolds (turbuelnt) stresses tensor (rst)
    def turbulent_stresses(self):
        # enforce use of fluctuating fields
        self = _enforce_flucs(self)
        self.rst = {}
        for i, in self.velocities:
            for j in self.velocities:
                if j >= i:
                    self.rst[i+j] = np.mean(np.multiply(self.flucfield[i], \
                            self.flucfield[j]), axis = self.namedaxes['t'])
    
    # calculate gradients of each component of a field with respect to the coords
    def grad_fields(self, flowset):
        if not hasattr(self, 'gradient_fields'):
            self.gradients = {}
        temp = getattr(self, flowset)
        for fieldkey in temp:
            for coordkey in self.coordinates:
                self.gradients['d'+fieldkey+'d'+coordkey] = \
                np.gradient(temp[fieldkey], np.unique(self.coordinates[coordkey]), \
                            axis = self.namedaxes[coordkey])
        
        
    #%% FlowField utility functions
    # list dict elements of FlowField object and associate keys
    def who(self):
        for key in self.__dict__.keys():
            if type(self.__dict__[key]) is dict:
                print(key,list(self.__dict__[key].keys()))
                
    #### flow visualization
    # 2D contour plot: coords = ['y', 'z'], val = 'U'
    def contourf(self, coords, val):
        fig = plt.figure
        a = self.coordinates[coords[0]]
        b = self.coordinates[coords[1]]
        plt.contourf(a, b, val, 32)
        plt.axis('scaled')
        plt.xlabel(coords[0])
        plt.ylabel(coords[1])
        plt.colorbar()
        plt.tight_layout
        plt.show()
        return fig


#%% FlowField utility functions
def _enforce_flucs(flowfield):
    """
    enforce the usage of fluctuating velocity fields
    """
    if 'flucfield' not in flowfield.__dict__:
        flowfield.velocity_flucs()
    return flowfield
   

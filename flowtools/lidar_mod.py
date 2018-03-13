#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  10:44:24 2018

Lidar scan object creator within the FlowTools package.

@author: nhamilto
@contact: nicholas.hamilton@nrel.gov
@version: v.0.1
"""
import numpy as np

class lidar_scan():
    '''
    class for scanning lidar images
    '''

    def __init__(self):
        self.ulos = np.zeros()
        self.range = np.zeros()
        self.azimuth = np.zeros()





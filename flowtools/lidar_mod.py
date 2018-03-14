#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  10:44:24 2018

Lidar scan object creator within the FlowTools package.

@author: nhamilto
@contact: nicholas.hamilton@nrel.gov
@version: v.0.1
"""

import tarfile
import os
import numpy as np

class lidarscan():
    """
    each lidar scan is an object constructed from input data.
    Most often, data are stored as tarballs, so individual scans must be 
    extracted from the set zipped together
    """

    def __init__(self, filename):
        
        with open(datafile, encoding='latin-1') as f:
            data = [line.rstrip('\r\n') for line in f]
            
        # extract header
        headlines = int(data[0].split('=')[-1])
        self.header = data[0:headlines]
        
        # extract range gates
        ranges = [line.split('\t') for line in header if 'altitudes' in line.lower()]
        self.ranges = ranges[0][1:]
        
        # extracte data
        colnames = data[headlines].split('\t')

        temp = data[headlines+1:]
        testdata = np.zeros()
        for il, line in enumerate(temp):
            testdata[il] = line.split('\t')
        testdata = np.asarray(testdata)

        self.timestamp = testdata[:,0]
        # radial wind speed
        rwscols = [ic for ic, k in enumerate(colnames) if 'Radial Wind Speed (m/s)' in k]
        self.rws = testdata[:,rwscols].astype('float')
        # dispersion
        dispcols = [ind for ind,k in enumerate(colnames) if 'Dispersion' in k]
        self.disp = testdata[:,dispcols].astype('float')
        # carrier to noise ratio
        cnrcols = [ind for ind,k in enumerate(colnames) if 'Carrier To Noise Ratio' in k]
        self.cnr = testdata[:,cnrcols].astype('float')
        # scan azimuth
        azcol = [ind for ind,k in enumerate(colnames) if 'Azimuth Angle' in k]
        self.azimuth = testdata[:,azcol].astype('float')
        # lidar compass heading
        compassheading = [k for k in header if 'Compass Heading' in k]
        self.compassheading = compassheading.split('=')[-1]
        # elevation angle
        elevation = [k for k in header if 'Elevation Angle 1' in k]
        self.elevation = elevation.split('=')[-1]

    def rws2hws(rws, azimuth):
        """
        convert radial wind speed (line of sight) to horizontal wind speed
        ax = b
        x: bulk velocity vector, {u, v}
        a: coefficient matrix
        b: ordinate 
        """
        pass


    # def _parse_header(header):
    #     """extract header info"""
    #     azmin = [k for k in header if 'Azimuth Angle 1' in k]
    #     azmin = azmin.split('=')[-1]

    #     azmax = [k for k in header if 'Azimuth Angle 2' in k]
    #     azmax = azmax.split('=')[-1]

    #     compassheading = [k for k in header if 'Compass Heading' in k]
    #     self.compassheading = compassheading.split('=')[-1

    #     azmax = [k for k in header if 'Azimuth Angle 2' in k]
    #     azmax = azmax.split('=')[-1]

    #     self.azimuth = np.linspace(azmin,axmax, )

    # def _loadscan(filename):
    #     """
    #     lidar output files include a header with lots of important info and
    #     a large array that has radial wind speed (rws), dispersion (disp), and
    #     carrier to noise ratio (cnr) as a function of time and range gate
    #     """
    #     with open(datafile, encoding='latin-1') as f:
    #         data = [line.rstrip('\r\n') for line in f]
            
    #     # extract header
    #     headlines = int(data[0].split('=')[-1])
    #     header = data[0:headlines]
        
    #     # extract range gates
    #     ranges = [line.split('\t') for line in header if 'altitudes' in line.lower()]
    #     ranges = ranges[0][1:]
        
    #     # extracte data
    #     colnames = data[headlines].split('\t')

    #     temp = data[headlines+1:]
    #     testdata = np.zeros()
    #     for il, line in enumerate(temp):
    #         testdata[il] = line.split('\t')
    #     testdata = np.asarray(testdata)

    #     timestamp = testdata[:,0]

    #     rwscols = [ic for ic, k in enumerate(colnames) if 'Radial Wind Speed (m/s)' in k]
    #     rws = testdata[:,rwscols].astype('float')

    #     dispcols = [ind for ind,k in enumerate(colnames) if 'Dispersion' in k]
    #     disp = testdata[:,dispcols].astype('float')

    #     cnrcols = [ind for ind,k in enumerate(colnames) if 'Carrier To Noise Ratio' in k]
    #     cnr = testdata[:,cnrcols].astype('float')

    #     azcol = [ind for ind,k in enumerate(colnames) if 'Azimuth Angle' in k]
    #     azimuth = testdata[:,azcol].astype('float')

    #     return timestamp, ranges, rws, disp, cnr, header, azimuth

def untar(tarfilename, format='r:*'):
        '''read data from tarball with given format'''
        tarobj = tarfile.open(tarfilename, format)
        assert tarobj.is_tarfile() 
        
        tarobj.extractall('temp')
        here = os.getcwd()
        templist = os.listdir(os.path.join(here,'temp'))
        datafiles = [item for item in templist if '.rtd' in item]

        # datafiles = os.path.join(os.path.join(here,'temp/2013_07_17__01_21_12/'),testfile)
        return datafiles
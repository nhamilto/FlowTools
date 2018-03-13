'''
read write compressed data
'''
import tarfile
import os
import numpy as np

def load(filename, format):
    '''read data from tarball with given format'''
    tarobj = tarfile.open(filename, format)
    assert datfile.is_tarfile() 
    
    tarobj.extractall('temp')
    here = os.getcwd()
    templist = os.listdir(os.path.join(here,'temp'))
    datafiles = [item for item in templist if '.rtd' in item]

    datafile = os.path.join(os.path.join(here,'temp/2013_07_17__01_21_12/'),testfile)
    with open(datafile, encoding='latin-1') as f:
        data = [line.rstrip('\r\n') for line in f]
        
        # extract header
        headlines = int(data[0].split('=')[-1])
        header = data[0:headlines]
        
        # extract range gates
        ranges = [line.split('\t') for line in header if 'altitudes' in line.lower()]
        ranges = ranges[0][1:]
        
        # extracte data
        colnames = data[headlines].split('\t')

        testdata = data[headlines+1:]
        for il, line in enumerate(testdata):
            testdata[il] = line.split('\t')
        testdata = np.asarray(testdata)

        rws = {k: testdata[:,ind] for ind,k in enumerate(colnames) if 'Radial Wind Speed (m/s)' in k}
        disp = {k: testdata[:,ind] for ind,k in enumerate(colnames) if 'Dispersion' in k}
        cnr = {k: testdata[:,ind] for ind,k in enumerate(colnames) if 'Carrier To Noise Ratio' in k}

    return rws, disp, cnr


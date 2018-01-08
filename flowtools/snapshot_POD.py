#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 08:34:50 2018

Snapshot Proper Orthogonal Decomposition module within the FlowTools package.

@author: nhamilto
@contact: nicholas.hamilton@nrel.gov
@version: v.0.1
"""
import numpy as np
import matplotlib.pyplot as plt

#%%
def decompose(flowfield):
    """
    decompose a fluctuating velocity field into eigenfunctions (POD['modes'])
    and their associated eigenvalues (POD['lam']) that express their energy in
    snapshot basis.
    The POD dict is returned as an attribute of the flowfield object. 
        type(flowfield.POD) = dict
    """
    # enforce use of fluctuating fields
    flowfield = _enforce_flucs(flowfield)
    # concatenate fluctuating velocity fields
    npoints = 1
    for coordkey in flowfield.coordinates:
        if coordkey not in ['t']:
            npoints = npoints*flowfield.npts[coordkey]
    uStack = np.zeros([0, flowfield.npts['t']])
    for key in flowfield.flucfield:
        uStack = np.concatenate((uStack, np.reshape(flowfield.flucfield[key], [npoints, flowfield.npts['t']])), axis = 0)
    # correlation matrix
    C = np.dot(uStack.transpose(), uStack)/flowfield.npts['t']
    
    # eigenvalue decomposition
    val, vec = np.linalg.eig(C)
    # project onto velocity fields to find modes
    phi = np.dot(uStack, vec)
    # normalize each mode by its respective L2-norm
    for mode in range(flowfield.npts['t']):
        phi[:, mode] = phi[:, mode]/np.linalg.norm(phi[:, mode], 2)
    # unpack modes 
    flowfield.POD = {'modes': {}}; temp = 0
    for key in flowfield.flucfield:
        flowfield.POD['modes'][key] = np.reshape(phi[temp*npoints:(temp+1)*npoints, :], flowfield.flucfield[key].shape)
        temp += 1
    # eigenvalues
    flowfield.POD['lam'] = np.real(val)
    flowfield.POD['lamnorm'] = flowfield.POD['lam']/np.sum(flowfield.POD['lam'])

#### coefficients
def calc_coefficients(flowfield, nmodes = None):
    """
    calculate the POD mode coefficients (POD['coeff']) that express the 
    amplitude of each mode in time.
    """
    # enforce use of fluctuating fields
    flowfield = _enforce_flucs(flowfield)
    # modes of interest
    nmodes = _parse_modes(flowfield, nmodes)
    # project velocity snapshots onto mode basis and integrate over domain
    integrand = 0
    for key in flowfield.flucfield:
        integrand += flowfield.POD['modes'][key][..., nmodes, np.newaxis]*flowfield.flucfield[key][..., np.newaxis, :]
    for coordkey in sorted(flowfield.namedaxes, key=flowfield.namedaxes.get):
        if coordkey == 't':
            continue
        integrand = np.trapz(integrand, x=np.unique(flowfield.coordinates[coordkey]), axis = 0)
    flowfield.POD['coeff'] = integrand

#### low dimensional description of Reynolds stresses
def recompose_rst(flowfield, nmodes = None):
    """
    reduced-order description of the turbulence field. Filters the Reynolds
    stress tensor by truncating the POD mode basis. 
    """
    # modes of interest
    nmodes = _parse_modes(flowfield, nmodes)
    flowfield.POD['rst'] = {}
    for i in flowfield.POD['modes']:
        for j in flowfield.POD['modes']:
            if j >= i:
                temp = np.multiply(flowfield.POD['modes'][i][..., nmodes], flowfield.POD['modes'][j][..., nmodes])
                flowfield.POD['rst'][i+j] = np.sum(np.multiply(temp, flowfield.POD['lam'][np.newaxis, np.newaxis, nmodes]), axis = -1)
                
def recompose_flucfield(flowfield, nmodes = None):
    """
    reduced-order description of the turbulence field. Filters the fluctuating
    velocity field by truncating the POD mode basis and combinging with the
    respective coefficients. 
    """
    # modes of interest
    nmodes = _parse_modes(flowfield, nmodes)
    flowfield.POD['vel_field_rec']={}
    for key in flowfield.POD['modes']:
#        temp1 = np.reshape()
#        temp2 = np.reshape()
#        print(temp1.shape)
#        print(temp2.shape)
        flowfield.POD['vel_field_rec'][key] = np.sum(flowfield.POD['modes'][key][..., nmodes, np.newaxis] * flowfield.POD['coeff'][np.newaxis, np.newaxis, ...], axis = 2)

# POD plotting function to check eigenvalues
def check_lam(flowfield):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (7,2.5))
    # normalized eigenvalues
    ax1.plot(np.arange(len(flowfield.POD['lamnorm'])), flowfield.POD['lamnorm'])
    ax1.set_xlabel('mode number, $n$')
    ax1.set_ylabel('$\lambda_n / \sum_{n=0}^{N} \lambda_n$')
    # cumulative summation of normalized eigenvalues
    ax2.plot(np.arange(len(flowfield.POD['lamnorm'])), flowfield.POD['lamnorm'].cumsum())
    ax2.set_xlabel('mode number, $N_r$')
    ax2.set_ylabel('$\sum_{n=0}^{N_r} \lambda_n / \sum_{n=0}^{N} \lambda_n$')
    fig.tight_layout()
    # modes required to reach thresholds of tke
    l50 = np.argmin(abs(flowfield.POD['lamnorm'].cumsum() - 0.5))
    l75 = np.argmin(abs(flowfield.POD['lamnorm'].cumsum() - 0.75))
    l95 = np.argmin(abs(flowfield.POD['lamnorm'].cumsum() - 0.9))
    # output text to screen
    print('Out of a total of', len(flowfield.POD['lam']), 'modes,')
    print(l50, 'modes needed to reach 50% tke')
    print(l75, 'modes needed to reach 75% tke')
    print(l95, 'modes needed to reach 95% tke')
    return fig, ax1, ax2

# POD plotting function to check coefficients
def coeff_plot(flowfield, nmodes = None):
    # modes of interest
    nmodes = _parse_modes(flowfield, nmodes)
    fig, axs = plt.subplots(len(nmodes), 1, sharex=True, figsize = (5, 1.25*len(nmodes)))
    pt = 0; labelx = -0.175  # axes coords
    for nm in nmodes:
        axs[pt].plot(flowfield.POD['coeff'][nm,:])
        axs[pt].set_ylabel('$a_{'+str(nm)+'}$')
        axs[pt].yaxis.set_label_coords(labelx, 0.5)
        pt += 1
    plt.xlabel('$t$')
    fig.tight_layout()
    return fig, axs

#%% POD utility functions
def _enforce_flucs(flowfield):
    """
    enforce the usage of fluctuating velocity fields
    """
    if 'flucfield' not in flowfield.__dict__:
        flowfield.velocity_flucs()
    return flowfield

def _parse_modes(flowfield, nmodes):
    """
    parse which modes to use to calculate coefficients, describe flowfield,
    make plots.
    """
    if nmodes is None:
        nmodes = np.argmin(abs(flowfield.POD['lamnorm'].cumsum() - 0.5))
        print('Defaulting to', nmodes, 'modes for 50% tke')
        nmodes = np.arange(nmodes)
    elif isinstance(nmodes, int):
        print('Using coefficients up to mode', nmodes)
        nmodes = np.arange(nmodes)
    elif isinstance(nmodes, (list, np.ndarray)):
        print('Using coefficients for modes:', list(nmodes))
    return nmodes
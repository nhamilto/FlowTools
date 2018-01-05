#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 12:01:56 2018

Flow Visualization module within the FlowTools package.

@author: nhamilto
@contact: nicholas.hamilton@nrel.gov.
@version: v.0.1
"""

import matplotlib.pyplot as plt
import numpy as np

#%%
# 2D contour plot: coords = ['y', 'z'], val = flowfield.'U'
def contourf(flowfield, coords, cval):
    fig = plt.figure
    x, y = flowfield.coordinates[coords[0]], flowfield.coordinates[coords[1]]
    plt.contourf(x, y, cval, 32)
    plt.axis('scaled')
    plt.xlabel(coords[0])
    plt.ylabel(coords[1])
    plt.colorbar()
    plt.tight_layout
    plt.show()
    return fig

# Reynolds stresses in planes defined by x and y
def rst_contours(flowfield, coords, rst, commonscale=True, vmin=None, vmax=None):
    subplotindex = [0, 1, 2, 4, 5, 8]
    fig, axs = plt.subplots(3,3, figsize = (6.5, 5), sharex = True, sharey = True)
    axs = axs.ravel()
    x, y = flowfield.coordinates[coords[0]], flowfield.coordinates[coords[1]]
    if commonscale is True:
        # plot all subfigures on a common scale
        if vmin is None:
            vmin = np.min([ np.min(rst[key]) for key in rst.keys() ])
        if vmax is None:
            vmax = np.max([ np.max(rst[key]) for key in rst.keys() ]) 
        for pt, key in zip(subplotindex,rst):
            axs[pt].contourf(x, y, rst[key], vmin=vmin, vmax=vmax)
            axs[pt].set_title('$\overline{'+key+'}$')
            axs[pt].axis('equal'); axs[pt].set_adjustable('box-forced')
        # make hidden subplot with full data range for correct colorbar 
        fakedata = np.reshape(np.arange(np.prod(rst[key].shape)),rst[key].shape)
        fakedata = (fakedata - fakedata.min())/(fakedata.max() - fakedata.min())
        fakedata = fakedata*(vmax-vmin) + vmin
        axt = fig.add_axes([0.01,0.01,0.01,0.01])
        cf = axt.contourf(x, y, fakedata, 32, vmin=vmin, vmax=vmax)
        fig.colorbar(cf, ax=axs.ravel().tolist())
        axt.set_visible(not axt.get_visible)      
        # hide unwanted axes
        for pt in [3,6,7]:
            axs[pt].set_visible(not axs[pt].get_visible)
        # label super axes
        fig.text(0.5, 0.04, '$'+coords[0]+'$', ha='center')
        fig.text(0.05, 0.5, '$'+coords[1]+'$', va='center', rotation='vertical')
        return fig, axs
    else:
        # plot each subplot with a unique scale
        for pt, key in zip(subplotindex,rst):
            cf = axs[pt].contourf(x, y, rst[key])
            axs[pt].set_title('$\overline{'+key+'}$')
            fig.colorbar(cf, ax=axs[pt])
            axs[pt].axis('equal'); axs[pt].set_adjustable('box-forced')
            # hide unwanted axes
        for pt in [3,6,7]:
            axs[pt].set_visible(not axs[pt].get_visible)
        # label super axes
        fig.text(0.5, 0.04, '$'+coords[0]+'$', ha='center')
        fig.text(0.05, 0.5, '$'+coords[1]+'$', va='center', rotation='vertical')
        fig.tight_layout()
        return fig, axs
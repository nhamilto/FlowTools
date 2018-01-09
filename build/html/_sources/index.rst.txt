.. FlowTools documentation master file, created by
   sphinx-quickstart on Tue Jan  9 10:27:32 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FlowTools: analysis of fluid dynamics and wind energy data
=====================================

Author: `Nicholas Hamilton <mailto:nicholas.hamilton@nrel.gov>`_

This Python module provides a set of tools for:

1. Calculating fundamental properties of fluid flows, such as:
   
   * Mean and fluctuating flow fields
   * Gradient fields
   * Vorticity
   * ... more to come...

2. Analysis of turbulence:

   * RMS velocities
   * Reynolds stress tensor
   * ... more to come...

3. Numerical decomposition:

   * Proper Orthogonal Decomposition
      * decomposition into modal basis
      * eigenvalues
      * mode coefficients
      * reconstruction of velocity snapshots or of turbulent stresses

4. Basic flow visualization

The hope for this toolbox is to have a consistent and robust set of objects and functions that aid in the analysis of fluid dynamics and wind energy data using methods and algorithms that are well tested in the field.

ToDo:
   * add other decomposition methods (DMD, EMD, Fourier, etc...)
   * build on the visualization tools
   * add a wind energy package
   * consider more aerodynamic properties

Consider:
   * adding a data loading package
   * make compatible with other NREL toolboxes (Floris, SAMWICH Box, etc.)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ..Usage

   ..Samples

   Code



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

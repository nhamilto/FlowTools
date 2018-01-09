================
 FlowTools
================

FlowTools is a python package designed for the analysis of fluid flow data, including  of turbulent fluid dynamics and wind energy.

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
   - [ ] add other decomposition methods (DMD, EMD, Fourier, etc...)
   - [ ] build on the visualization tools
   - [ ] add a wind energy package
   - [ ] consider more aerodynamic properties

Consider:
   - [ ] adding a data loading package
   - [ ] make compatible with other NREL toolboxes (Floris, SAMWICH Box, etc.)


The main object class in FlowTools is the FlowField class. All other other functions operate on instances of this class. FlowField requires two inputs: (1) velocities - a dict containing instantaneous velocities u, v, w, of a common size, (2) coordinates - a dict containing the coordinates, x, y, z, t, of the data.


Acknowledgments
================
Thanks to anyone who would like to contribute! Please see below. 

License
================
Please read LICENSE for details on the license for use and sharing.

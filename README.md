# GeoNet
Geomorphic feature extraction from high resolution topography data. 

When using GeoNet, please cite the following papers:

Passalacqua, P., T. Do Trung, E. Foufoula-Georgiou, G. Sapiro, W. E. Dietrich (2010), A geometric framework for channel network extraction from lidar: Nonlinear diffusion and geodesic paths, Journal of Geophysical Research Earth Surface, 115, F01002, doi:10.1029/2009JF001254.

Sangireddy, H., R. A. Carothers, C.P. Stark, P. Passalacqua (2016), Controls of climate, topography, vegetation, and lithology on drainage density extracted from high resolution topography data, Journal of Hydrology, 537, 271-282, doi:10.1016/j.jhydrol.2016.02.051.


## Environment
``` conda env create -f GeoNetEnv.yml ```

#### Scikit-FMM Install
```git clone https://github.com/scikit-fmm/scikit-fmm.git```

```cd scikit-fmm```

```python setup.py install```

Note: This was done assuming scikit-fmm was cloned into your working directory.

## Configuration and Setup

Create a configuration file for your project using:

```python pygeonet_configure.py ```

#### Optional Arguments:

```-dir </path/to/GeoNet/Home_Directory>```

```-p [projectName]```

```-n [DEM_Name]```

```--input_dir [Input_Directory_Name]```

```--output_dir [Output_Directory_Name]```

Create a file structure based on the previous inputs:

```python pygeonet_prepare.py```

Default File Structure:
- GeoNet
  - GeoInputs
    - GIS
      - *Project Name (-p from configure step)*
        - dem.tif
  - GeoOutputs
    - GIS
      - *Project Name (-p from configure step)*
        - dem.tif
  - *** configuration file ***
  
  ## Scripts
  
  1. Perona-Malik non-linear, diffusion filter:
  
  ```python pygeonet_nonlinear_filter.py```
  
  2. Slope and Curvature:
  
  ```python pygeonet_slope_curvature.py```
  
  3. Flow Direction, Flow Accumulation, Outlets, and Basins
  
  ```python pygeonet_grass_py2.py``` or ```python pygeonet_grass_py2.py```
  
  If you have GRASS GIS 7.6 installed, used the first command. If you have GRASS GIS 7.8 installed, used the second command
  
  4. Flow Accumulation and Curvature Skeleton
  
  ```python pygeonet_skeleton_definition.py```
  
  5. Geodesic Minimum Cost Path and Fast Marching Algorithm
  
  ```python pygeonet_fast_marching.py```
  
  6. Channel Head Detection
  
  ```python pygeonet_channel_head_definition.py```
  
  Note: Further research still needs to be done on the optimal threshold for identifying channel heads. Preliminary studies found a threshold of 0.3 to be sufficient, but this estimate can definitely be improved using analytical methods.

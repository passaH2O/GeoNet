# GeoNet

## Environment
``` conda env create -f GeoNetEnv.yml ```

#### Scikit-FMM Install
```git clone https://github.com/scikit-fmm/scikit-fmm.git```

```cd scikit-fmm```

```python setup.py install```

Note: This was done assuming a scikit-fmm was cloned into your working directory

## Configuration and Setup

Create a configuration file for your project using:

``` python pygeonet_configure.py ```

#### Optional Arguments:

```-dir </path/to/GeoNet/Home_Directory>```

```-p [projectName]```

```-n [DEM_Name]```

```--input_dir [Input_Directory_Name]```

```--output_dir [Output_Directory_Name]```

Create a file structure based on the previous inputs:

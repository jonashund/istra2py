# istra2py

Read hdf5 files exported from Istra4D digital image correlation with python


## Install
- Install Python (e.g. [Install Anaconda])
- Install package
	- Development mode `python3 setup.py develop`
	- Non-development mode `python3 setup.py install`
- Remove package
	- Development mode `python3 setup.py develop --uninstall`
	- Non-development mode `python3 setup.py --uninstall`
	

## Example

### Input
```python
import istra2py

r = istra2py.Reader("data")
r._list_available_keys()
r.read()
```

### Output
```shell
Found the following files
['series_step_0.hdf5',
 'series_step_1.hdf5',
 'series_step_10.hdf5',
 'series_step_11.hdf5',
 'series_step_2.hdf5',
 'series_step_3.hdf5',
 'series_step_4.hdf5',
 'series_step_5.hdf5',
 'series_step_8.hdf5',
 'series_step_9.hdf5']

Sorted files are
['series_step_0.hdf5',
 'series_step_1.hdf5',
 'series_step_2.hdf5',
 'series_step_3.hdf5',
 'series_step_4.hdf5',
 'series_step_5.hdf5',
 'series_step_8.hdf5',
 'series_step_9.hdf5',
 'series_step_10.hdf5',
 'series_step_11.hdf5']

{'add_data': ['analog_channels'],
 'coordinates': ['coordinate_x',
                 'coordinate_x_var',
                 'coordinate_y',
                 'coordinate_y_var',
                 'coordinate_z',
                 'coordinate_z_var',
                 'distance_to_plane',
                 'distance_to_sphere',
                 'mask',
                 'variance_sphere'],
 'displacements': ['displacement_total',
                   'displacement_total_rbmr',
                   'displacement_total_rbmr_var',
                   'displacement_total_var',
                   'displacement_x',
                   'displacement_x_rbmr',
                   'displacement_x_var',
                   'displacement_y',
                   'displacement_y_rbmr',
                   'displacement_y_var',
                   'displacement_z',
                   'displacement_z_rbmr',
                   'displacement_z_var',
                   'mask'],
 'strains': ['mask',
             'strain_p1',
             'strain_p1_var',
             'strain_p2',
             'strain_p2_var',
             'strain_xx',
             'strain_xx_var',
             'strain_xy',
             'strain_xy_var',
             'strain_yy',
             'strain_yy_var']}
Processed basics are:
{'Coordinates': '.x',
 'Displacements': '.u',
 'Strains': '.eps',
 'Traverse displacement': '.traverse_displ',
 'Traverse force': '.traverse_force'}

Indices of basics are: [nbr_files, nbr_x, nbr_y, nbr_components] with
nbr_files =  10
nbr_x =  50
nbr_y =  49




```


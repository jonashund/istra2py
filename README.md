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

r = Reader(
    path_dir_acquisition=os.path.join("data", "acquisition"),
    path_dir_export=os.path.join("data", "export"),
    verbose=True
)
r.read(identify_images_export=True)

print("\nr.__dict__.keys()")
print(r.__dict__.keys())
print("\nr.acquisition.__dict__.keys()")
print(r.acquisition.__dict__.keys())
print("\nr.export.__dict__.keys()")
print(r.export.__dict__.keys())
```

### Output
```shell
Searched dir=data/acquisition

Found the following files
['series_step_0.hdf5',
 'series_step_1.hdf5',
 'series_step_10.hdf5',
 'series_step_11.hdf5',
 'series_step_2.hdf5',
 'series_step_3.hdf5',
 'series_step_4.hdf5',
 'series_step_5.hdf5',
 'series_step_6.hdf5',
 'series_step_7.hdf5',
 'series_step_8.hdf5',
 'series_step_9.hdf5']


Sorted files are
['series_step_0.hdf5',
 'series_step_1.hdf5',
 'series_step_2.hdf5',
 'series_step_3.hdf5',
 'series_step_4.hdf5',
 'series_step_5.hdf5',
 'series_step_6.hdf5',
 'series_step_7.hdf5',
 'series_step_8.hdf5',
 'series_step_9.hdf5',
 'series_step_10.hdf5',
 'series_step_11.hdf5']


Extracted attributes:
{'Images': '.images',
 'Traverse displacement': '.traverse_displ',
 'Traverse force': '.traverse_force'}

Indices of basics are: [nbr_files, nbr_x, nbr_y, nbr_components] with
nbr_files =  12
nbr_pix_x =  504
nbr_pix_y =  496

Searched dir=data/export

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


Extracted attributes:
{'Coordinates': '.x',
 'Displacements': '.u',
 'Strains': '.eps',
 'Traverse displacement': '.traverse_displ',
 'Traverse force': '.traverse_force'}

Indices of basics are: [nbr_files, nbr_x, nbr_y, nbr_components] with
nbr_files =  10
nbr_x =  50
nbr_y =  49


r.__dict__.keys()
dict_keys(['verbose', 'path_dir_acquisition', 'path_dir_export', 'acquisition', 'export', '_available_positions'])

r.acquisition.__dict__.keys()
dict_keys(['verbose', 'path_dir', '_file_ending', '_file_names_unsorted', '_file_names', 'paths_files', 'nbr_files', 'traverse_force', 'traverse_displ', 'images'])

r.export.__dict__.keys()
dict_keys(['verbose', 'path_dir', '_file_ending', '_file_names_unsorted', '_file_names', 'paths_files', 'nbr_files', 'traverse_force', 'traverse_displ', 'x', 'u', 'eps', 'image_indices', 'images'])


```


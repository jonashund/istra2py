#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import numpy as np
import pprint
import h5py


class Istra2pyException(Exception):
    pass


class Reader:
    def __init__(self, path_dir_acquisition=None, path_dir_export=None):
        self.path_dir_acquisition = path_dir_acquisition
        self.path_dir_export = path_dir_export

    def read(self,):
        if self.path_dir_acquisition:
            self.acquisition = AcquisitionReader(path_dir=self.path_dir_acquisition)
            self.acquisition.read()
        if self.path_dir_export:
            self.export = ExportReader(path_dir=self.path_dir_export)
            self.export.read()

    def get_images_of_exported_frames(self,):
        self._available_positions = {
            frozenset(pair): i
            for i, pair in enumerate(
                np.concatenate(
                    (r.acquisition.traverse_displ, r.acquisition.traverse_force), axis=1
                ),
            )
        }

        def get_position_if_available(key, index):
            try:
                return self._available_positions[key]
            except KeyError as e:
                print(
                    "Key={} \ncorresponding to export data at index={} \n"
                    "is not found in image-keys of acquisition data.\n"
                    "self.export.images[index] will contain only np.nan\n".format(
                        key, index
                    )
                )
                return None

        self.export.image_indices = indices = [
            get_position_if_available(key=frozenset(pair), index=i)
            for i, pair in enumerate(
                np.concatenate(
                    (r.export.traverse_displ, r.export.traverse_force), axis=1
                )
            )
        ]

        # self.export.images = self.acquisition.images[tuple(self._indices), :]
        # Does not handle "None" case, i.e. cases where no acquisition image
        # is available

        nbr_frames_export = len(indices)
        images = np.full((nbr_frames_export, *self.acquisition.images[0].shape), np.nan)
        for i, index in enumerate(indices):
            if index is not None:
                images[i, :] = self.acquisition.images[index, :]

        self.export.images = images


class ReaderDirectory:
    def __init__(self, path_dir):
        self.path_dir = path_dir
        self._file_ending = ".hdf5"

        self._file_names_unsorted = self._find_files_in_dir()
        self._file_names = self._sort_file_names()
        self.paths_files = [os.path.join(path_dir, name) for name in self._file_names]

        self.nbr_files = len(self.paths_files)

    def list_available_keys(self, file_index=1):
        with h5py.File(self.paths_files[file_index], "r") as first_file:
            d = {key: [k for k in first_file[key].keys()] for key in first_file.keys()}
            pprint.pprint(d)
            return d

    def _sort_file_names(self, verbose=False):
        # Find numbers directly in front of file ending
        regex = re.compile(r"(\d+)" + self._file_ending)
        numbers = [int(regex.findall(name)[0]) for name in self._file_names_unsorted]
        ordered_indices = np.array(numbers).argsort()

        file_names_sorted = np.array(self._file_names_unsorted)[
            ordered_indices
        ].tolist()

        if verbose:
            print("Sorted files are")
            pprint.pprint(file_names_sorted)
            print()

        return file_names_sorted

    def _find_files_in_dir(self, verbose=False):

        names = []
        for file in os.listdir(self.path_dir):
            if file.endswith(self._file_ending):
                names.append(file)
        names.sort()

        if not names:
            raise Istra2pyException(
                "No files with ending {} found in {}".format(
                    self._file_ending, self.path_dir
                )
            )

        if verbose:
            print("Found the following files")
            pprint.pprint(names)
            print()

        return names


class AcquisitionReader(ReaderDirectory):
    def read(self, verbose=False):
        key_main = "correlation_load_series_camera_1"
        key_images = "camera_pos_1"
        dtype_image = np.uint8

        nbr_files = self.nbr_files
        with h5py.File(self.paths_files[0], "r") as first_file:
            nbr_pix_x, nbr_pix_y = first_file[key_main][key_images].shape

        if verbose:
            print("Extracted attributes:")
            basics = {
                "Traverse force": ".traverse_force",
                "Traverse displacement": ".traverse_displ",
                "Images": ".images",
            }
            pprint.pprint(basics)
            print()

            print(
                "Indices of basics are: [nbr_files, nbr_x, nbr_y, nbr_components] with"
            )
            print("nbr_files = ", nbr_files)
            print("nbr_pix_x = ", nbr_pix_x)
            print("nbr_pix_y = ", nbr_pix_y)

        self.traverse_force = np.zeros((nbr_files, 1), dtype=np.float64)
        self.traverse_displ = np.zeros((nbr_files, 1), dtype=np.float64)
        self.images = np.zeros((nbr_files, nbr_pix_x, nbr_pix_y), dtype=dtype_image)

        for index_path, path in enumerate(self.paths_files):
            hdf5 = h5py.File(path, "r")

            analog = hdf5[key_main]["analog_channels"][0]
            self.traverse_force[index_path, 0] = analog[0]  # Is this correct?
            self.traverse_displ[index_path, 0] = analog[1]  # Is this correct?

            image = hdf5[key_main][key_images]
            self.images[index_path, :, :] = image

            hdf5.close()


class ExportReader(ReaderDirectory):
    def read(self, verbose=False):
        nbr_files = self.nbr_files

        with h5py.File(self.paths_files[0], "r") as first_file:
            nbr_x, nbr_y = first_file["coordinates"]["coordinate_x"].shape

        if verbose:
            print("Extracted attributes:")
            basics = {
                "Traverse force": ".traverse_force",
                "Traverse displacement": ".traverse_displ",
                "Coordinates": ".x",
                "Displacements": ".u",
                "Strains": ".eps",
            }
            pprint.pprint(basics)
            print()

            print(
                "Indices of basics are: [nbr_files, nbr_x, nbr_y, nbr_components] with"
            )
            print("nbr_files = ", nbr_files)
            print("nbr_x = ", nbr_x)
            print("nbr_y = ", nbr_y)

        self.traverse_force = np.zeros((nbr_files, 1), dtype=np.float64)
        self.traverse_displ = np.zeros((nbr_files, 1), dtype=np.float64)
        self.x = np.zeros((nbr_files, nbr_x, nbr_y, 2), dtype=np.float64)
        self.u = np.zeros((nbr_files, nbr_x, nbr_y, 2), dtype=np.float64)
        self.eps = np.zeros((nbr_files, nbr_x, nbr_y, 3), dtype=np.float64)

        for index_path, path in enumerate(self.paths_files):
            hdf5 = h5py.File(path, "r")

            analog = hdf5["add_data"]["analog_channels"][0]
            self.traverse_force[index_path, 0] = analog[0]  # Is this correct?
            self.traverse_displ[index_path, 0] = analog[1]  # Is this correct?

            coords = hdf5["coordinates"]
            self.x[index_path, :, :, 0] = coords["coordinate_x"][:, :]
            self.x[index_path, :, :, 1] = coords["coordinate_y"][:, :]

            disp = hdf5["displacements"]
            self.u[index_path, :, :, 0] = disp["displacement_x"][:, :]
            self.u[index_path, :, :, 1] = disp["displacement_y"][:, :]

            strain = hdf5["strains"]
            self.eps[index_path, :, :, 0] = strain["strain_xx"][:, :]
            self.eps[index_path, :, :, 1] = strain["strain_yy"][:, :]
            self.eps[index_path, :, :, 2] = strain["strain_xy"][:, :]

            hdf5.close()


if __name__ == "__main__":
    r_e = ExportReader(os.path.join("data", "export"))
    r_e.read()

    r_a = AcquisitionReader(os.path.join("data", "acquisition"))
    r_a.read()

    r = Reader(
        path_dir_acquisition=os.path.join("data", "acquisition"),
        path_dir_export=os.path.join("data", "export_skipping_some_frames"),
        # path_dir_export=os.path.join("data", "export_skipping_some_frames"),
    )
    r.read()

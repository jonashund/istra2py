#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run tests:
    python -m pytest
"""

import os
import sys
import pytest
import h5py
import runpy
import pathlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),)
import istra2py


##############################################


@pytest.fixture
def exportReader():
    return istra2py.ExportReader(os.path.join("data", "export"))


@pytest.fixture
def acquisitionReader():
    return istra2py.AcquisitionReader(os.path.join("data", "acquisition"))


@pytest.fixture
def reader():
    return istra2py.Reader(
        path_dir_acquisition=os.path.join("data", "acquisition"),
        path_dir_export=os.path.join("data", "export"),
        verbose=True,
    )


@pytest.fixture
def reader_ready(reader):
    reader.read(identify_images_export=True)
    return reader


@pytest.fixture
def reader_skipping():
    return istra2py.Reader(
        path_dir_acquisition=os.path.join("data", "acquisition"),
        path_dir_export=os.path.join("data", "export_skipping_some_frames"),
        verbose=True,
    )
    # path_dir_export=os.path.join("data", "export_skipping_some_frames"),
    # r.read(identify_images_export=False)


class Test_init:
    def test_init(self, reader):
        assert hasattr(reader, "read")

    def test_init_export(self, exportReader):
        reader = exportReader
        assert hasattr(reader, "read")

    def test_init_acquisitionReader(self, acquisitionReader):
        reader = acquisitionReader
        assert hasattr(reader, "read")

    def test_init_nonexisting_dir(self,):
        with pytest.raises(FileNotFoundError):
            istra2py.ExportReader("data_not_existing_124376124")

    def test_init_empty_dir(self,):
        with pytest.raises(istra2py.Istra2pyException):
            istra2py.ExportReader("data_empty")

    def test_read(self, reader):
        reader.read(identify_images_export=False)
        assert hasattr(reader, "export")
        assert hasattr(reader, "acquisition")
        assert not hasattr(reader.export, "images")


class Test_read:
    def test_read_and_identify_images(self, reader):
        reader.read(identify_images_export=True)
        assert hasattr(reader.export, "images")

    def test_read_skipping_and_identify_images(self, reader_skipping):
        reader = reader_skipping
        reader.read(identify_images_export=True)
        assert hasattr(reader.export, "images")


class Test_core:
    def test_list_available_keys(self, exportReader):
        reader = exportReader
        assert reader.list_available_keys() is not None

    def test_get_single_hdf5_file(self, reader_ready):
        reader = reader_ready
        assert type(reader.export.get_single_hdf5_file()) == h5py._hl.files.File


################################
# Scripts


@pytest.mark.parametrize(
    "script",
    pathlib.Path(os.path.dirname(__file__), "..", "scripts").resolve().glob("*.py"),
)
def test_script_execution(script):
    runpy.run_path(script)
    assert True


if __name__ == "__main__":
    pass

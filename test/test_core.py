#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run tests:
    python -m pytest
"""

import os
import sys
import pytest

sys.path.append(os.path.join(".."))
import istra2py


##############################################


@pytest.fixture
def exportReader():
    return istra2py.ExportReader(os.path.join("data", "export"))


@pytest.fixture
def reader():
    return istra2py.Reader(
        path_dir_acquisition=os.path.join("data", "acquisition"),
        path_dir_export=os.path.join("data", "export"),
        verbose=True,
    )


@pytest.fixture
def reader_skipping():
    return istra2py.Reader(
        path_dir_acquisition=os.path.join("data", "acquisition"),
        path_dir_export=os.path.join("data", "export_skipping_some_frames"),
        verbose=True,
    )
    # path_dir_export=os.path.join("data", "export_skipping_some_frames"),
    # r.read(identify_images_export=False)


@pytest.fixture
def acquisitionReader():
    return istra2py.AcquisitionReader(os.path.join("data", "acquisition"))


class Test_core:
    def test_init(self, reader):
        assert reader is not None
        return reader

    def test_read(self, reader):
        reader.read(identify_images_export=False)

    def test_read_and_identify_images(self, reader):
        reader.read(identify_images_export=True)

    def test_read_skipping_and_identify_images(self, reader_skipping):
        reader = reader_skipping
        reader.read(identify_images_export=True)

    def test_init_export(self, exportReader):
        reader = exportReader
        assert reader is not None

    def test_init_acquisitionReader(self, acquisitionReader):
        reader = acquisitionReader
        assert reader is not None

    def test_init_nonexisting_dir(self,):
        with pytest.raises(FileNotFoundError):
            istra2py.ExportReader("data_not_existing_124376124")

    def test_init_empty_dir(self,):
        with pytest.raises(istra2py.Istra2pyException):
            istra2py.ExportReader("data_empty")

    def test_list_available_keys(self, exportReader):
        reader = exportReader
        exportReader.list_available_keys()


if __name__ == "__main__":
    r = Test_core().test_init(reader=reader)

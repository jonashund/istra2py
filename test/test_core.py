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
def exportReaderSkipped():
    return istra2py.ExportReader(os.path.join("data", "export_skipping_some_frames"))


@pytest.fixture
def acquisitionReader():
    return istra2py.ExportReader(os.path.join("data", "acquisition"))


class Test_core:
    def test_init_export(self, exportReader):
        assert exportReader is not None

    def test_init_exportReaderSkipped(self, exportReaderSkipped):
        assert exportReaderSkipped is not None

    def test_init_acquisitionReader(self, acquisitionReader):
        assert acquisitionReader is not None

    def test_init_nonexisting_dir(self,):
        with pytest.raises(FileNotFoundError):
            istra2py.ExportReader("data_not_existing_124376124")

    def test_init_empty_dir(self,):
        with pytest.raises(istra2py.Istra2pyException):
            istra2py.ExportReader("data_empty")

    def test_list_available_keys(self, exportReader):
        exportReader.list_available_keys()


if __name__ == "__main__":
    Test_core().test_init()

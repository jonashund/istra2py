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
def reader():
    return istra2py.Reader("data")


class Test_core:
    def test_init(self, reader):
        pass

    def test_init_nonexisting_dir(self,):
        with pytest.raises(FileNotFoundError):
            istra2py.Reader("data_not_existing_124376124")

    def test_init_empty_dir(self,):
        with pytest.raises(istra2py.Istra2pyException):
            istra2py.Reader("data_empty")

    def test_list_available_keys(self, reader):
        reader._list_available_keys()


if __name__ == "__main__":
    Test_core().test_init()

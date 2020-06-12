#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run tests:
    python -m pytest
"""

import os
import sys

sys.path.append(os.path.join(".."))
import istra2py


##############################################


class Test_core:
    def test_init(self,):
        istra2py.Reader("data")


if __name__ == "__main__":
    Test_core().test_init()

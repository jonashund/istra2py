#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Run tests:
    python -m pytest
"""

import os
import sys

sys.path.append(os.path.join(".."))
import istra2py


##########################################
# Tests

class Test_Dummy:
    def test_foo(self,):
        assert True


if __name__ == "__main__":
    Test_Dummy().test_foo()

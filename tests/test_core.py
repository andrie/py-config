import os
import pytest
from config import *


def test_core():
    assert get_env('TEST') == 'default'
    os.environ['TEST'] = 'test'
    assert get_env('TEST') == 'test'

    # assert "fail" == "pass"
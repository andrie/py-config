import os
import pytest
from config import *
from config.core import read_yaml


def test_get_env():
    assert get_env('TEST') == 'default'
    os.environ['TEST'] = 'test'
    assert get_env('TEST') == 'test'

    # assert "fail" == "pass"

def test_config_get():
    assert config_get('trials') == 5
    assert config_get('trials', 'production') == 30


def test_read_yaml():
    #| hide
    x = read_yaml(
        """
        trials: 1
        expr: !expr os.getcwd()
        # expr2: !expr invalid()
        """
    )
    assert x['trials'] == 1
    assert x['expr'] == os.getcwd()

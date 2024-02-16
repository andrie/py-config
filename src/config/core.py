"""
This module is inspired by the `config` library for R.
See https://github.com/rstudio/config.

"""




import yaml
import os
import pathlib
import inspect
import traceback
import warnings

from typing import Any, Union, Tuple


def get_env(
        var:str, 
        default:str = "default" 
    ) -> str:
    """
    Get a value from the environment variables.

    Paramaters
    ----------
    var: str
        The environment variable to get
    default: str
        The default value to return if the environment variable is not set

    """
    return os.environ.get(var, "default")




def find_config_file(file, depth = 3):
    sources = {
        inspect.stack()[0][1],
        os.path.dirname(traceback.extract_stack()[-depth].filename),
        os.getcwd(),
        os.path.abspath(""),
    }

    file_exists = False
    for source in sources:
        filename = pathlib.Path(source, file)
        if os.path.exists(filename):
            file_exists = True
            # print(f"Found file {file} with source {source}")
            break

        else:
            # print(f"File {file} not found with source {source}")
            pass

    if not file_exists:
        source_locs = '\n - '.join(sources)
        raise FileNotFoundError(f"File {file} not found in any of these locations: \n - {source_locs}")
    
    return filename

# find_config_file("config.yaml")

def expr_constructor(loader, node):
    value = loader.construct_scalar(node)
    z = None
    try:
        z = eval(value)
    except:
        # import warnings
        def format_warning(message, category, filename, lineno, file=None, line=None):
            return ' %s:%s:\n %s:%s' % (filename, lineno, category.__name__, message)
        warnings.formatwarning = format_warning
        msg = f" Cannot evaluate expression in config.yaml: `{value}`"
        warnings.warn(msg, stacklevel=0)
    
    return z


def read_yaml(file):
    yaml.add_constructor('!expr', expr_constructor)
    return yaml.load(file, Loader=yaml.Loader)




def config_get(
        value: str = None, # Name of value (None to read all values)
        py_config_active:str = None, # Name of configuration to read from. Defaults to the value of the `R_CONFIG_ACTIVE` environment variable ("default" if the variable does not exist).
        file:str = 'config.yaml', # Configuration file to read from.
        encoding:str = None
    ):
    """Get a value from the `config.yaml` file.

    Read from the currently active configuration, retrieving either a single named value or all values as a list.
    
    Parameters
    ----------
    value: str, optional
        Name of value (None to read all values)
    py_config_active: str, optional
        Name of configuration to read from. Defaults to the value of the `R_CONFIG_ACTIVE` environment variable ("default" if the variable does not exist).
    file: str
        Configuration file to read from.
    encoding: str
        Encoding to use when reading the file. Defaults to "utf-8".
    
    """
    if py_config_active is None:
        py_config_active = get_env('R_CONFIG_ACTIVE', 'default')
    
    filename = find_config_file(file)

    dir_path = os.getcwd()
    file = pathlib.Path(dir_path, filename)

    with open(file, 'r', encoding = encoding) as stream:
        conf = read_yaml(stream)
    
    if value is None:
        return conf[py_config_active]
    else:
        return conf[py_config_active][value]


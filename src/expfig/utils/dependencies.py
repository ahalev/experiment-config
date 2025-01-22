import importlib

class BadModule:
    def __init__(self, module):
        self.module = module

    def __getattr__(self, item):
        if item.startswith('__'):
            # Alleviates pytest issue with self.__unwrapped__, see https://github.com/pytest-dev/pytest/issues/5080
            raise AttributeError(item)

        raise ModuleNotFoundError(f"Optional dependency '{self.module}' not installed. "
                                  f"Install with e.g. 'pip install {self.module}' to utilize this functionality.")


def load_module(module):
    try:
        if module == 'numpy':
            import numpy as m
        elif module == 'pandas':
            import pandas as m
        else:
            m = importlib.import_module(module)
    except ImportError:
        return BadModule(module)

    return m


def _get_pandas():
    try:
        import pandas as pd
    except ImportError:
        return BadModule('pandas')
    else:
        return pd


pandas = load_module('pandas')

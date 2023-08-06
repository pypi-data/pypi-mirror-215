import os
from abc import ABC


class Configuration(ABC):
    """
    This Configuration Class holds all the necessary functionality and constants of Robot Tool.
    """
    ROOT_BASE_PATH = str(os.path.join(
        os.path.realpath(''), "test23/tests"))

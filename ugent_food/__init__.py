from datetime import datetime

from .config import Config
from .menu import menu_for


def main(argv=None):
    _config = Config.load()

    # print(argv)
    menu_for(datetime.now(), _config)

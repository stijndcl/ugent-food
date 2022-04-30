from datetime import datetime

from .config import Config
from .exceptions import NoMenuFoundException
from .menu import menu_for


def main(argv=None):
    _config = Config.load()

    try:
        menu_for(datetime.now(), _config).print_menu(_config)
    except NoMenuFoundException as e:
        print(str(e))

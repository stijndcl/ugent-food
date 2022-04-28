from datetime import datetime

from .data.enums import Language
from .i18n import Translator
from .menu import menu_for


def main(argv=None):
    translator = Translator(Language.EN)

    # print(argv)
    menu_for(datetime.now(), translator)

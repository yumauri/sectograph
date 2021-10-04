from PyQt5 import QtGui
from .locator import Fonts


class Font:
    db: QtGui.QFontDatabase

    def __init__(self, family: str) -> None:
        self.db = QtGui.QFontDatabase()
        for font in Fonts.all()[family]:
            self.db.addApplicationFont(font)

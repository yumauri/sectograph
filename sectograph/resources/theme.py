import darkdetect
import json
from PyQt5 import QtCore
from .locator import Themes


def getter(obj):
    def locator(*path):
        cur = obj
        for p in path:
            if type(cur) == dict and p in cur:
                cur = cur[p]
            elif type(cur) == list and p < len(cur):
                cur = cur[p]
            else:
                return None
        return cur

    return locator


class NoThemeException(Exception):
    pass


class Theme:
    def __init__(self) -> None:
        self.themes = {}
        for name, path in Themes.all().items():
            # use QFile instead of simple `open` to get file from .rcc resources
            file = QtCore.QFile(path)
            if file.exists():
                try:
                    if file.open(QtCore.QFile.ReadOnly):
                        source = bytes(file.readAll()).decode("utf-8")
                        self.themes[name] = json.loads(source)
                    else:
                        print(f"Error: cannot open theme '{name}' file '{path}'")
                except Exception as err:
                    print(f"Error: cannot load theme '{name}':", err)
            else:
                print(f"Error: theme '{name}' file '{path}' doesn't exists")

    def get(self, name: str, *path):
        if name in self.themes:
            get = getter(self.themes[name])
        elif darkdetect.isDark() and name + "-dark" in self.themes:
            get = getter(self.themes[name + "-dark"])
        elif name + "-light" in self.themes:
            get = getter(self.themes[name + "-light"])
        else:
            raise NoThemeException(f"Error: no theme '{name}'")
        return getter(get(*path)) if path else get

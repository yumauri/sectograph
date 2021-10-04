from __future__ import annotations
from PyQt5 import QtCore, QtMultimedia
from .locator import Sounds


class Sound:
    sounds: dict[str, QtMultimedia.QSoundEffect]

    def __init__(self) -> None:
        self.sounds = {}
        for name, file in Sounds.all().items():
            url = QtCore.QUrl.fromLocalFile(file)
            self.sounds[name] = QtMultimedia.QSoundEffect()
            self.sounds[name].setSource(url)
            self.sounds[name].setVolume(0.5)
            self.sounds[name].setLoopCount(1)
            # self.sounds[name] = QtMultimedia.QSound(self.sounds["Chime"])
            # self.sounds[name].setLoops(1)

    def play(self, name: str = "Chime") -> None:
        if name not in self.sounds:
            name = "Chime"
        self.sounds[name].play()

    def names(self) -> list[str]:
        return list(self.sounds.keys())

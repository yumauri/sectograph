from __future__ import annotations
from PyQt5 import QtCore


# load resource binary file
# package_directory = os.path.dirname(os.path.abspath(__file__))
path = "sectograph/resources"
QtCore.QResource.registerResource(path + "/rc.rcc")


class Icons:
    color = ":/icons/icon-color.svg"
    bw = ":/icons/icon-bw.svg"
    bw_fill = ":/icons/icon-bw-fill.svg"

    @staticmethod
    def all() -> dict[str, str]:
        return {
            "color": Icons.color,
            "bw": Icons.bw,
            "bw-fill": Icons.bw_fill,
        }


class Themes:
    default_light = "default-light.json"
    default_dark = "default-dark.json"

    @staticmethod
    def all() -> dict[str, str]:
        return {
            "default-light": ":/themes/" + Themes.default_light,
            "default-dark": ":/themes/" + Themes.default_dark,
        }


class Fonts:
    raleway = [
        "Raleway-Black.ttf",
        "Raleway-BlackItalic.ttf",
        "Raleway-Bold.ttf",
        "Raleway-BoldItalic.ttf",
        "Raleway-ExtraBold.ttf",
        "Raleway-ExtraBoldItalic.ttf",
        "Raleway-ExtraLight.ttf",
        "Raleway-ExtraLightItalic.ttf",
        "Raleway-Italic.ttf",
        "Raleway-Light.ttf",
        "Raleway-LightItalic.ttf",
        "Raleway-Medium.ttf",
        "Raleway-MediumItalic.ttf",
        "Raleway-Regular.ttf",
        "Raleway-SemiBold.ttf",
        "Raleway-SemiBoldItalic.ttf",
        "Raleway-Thin.ttf",
        "Raleway-ThinItalic.ttf",
        "Raleway-ThinItalic.ttf",
        "Reallyway.ttf",  # modified Raleway-Regular font with 70% line-height from original
    ]

    @staticmethod
    def all() -> dict[str, list[str]]:
        return {
            "raleway": list(map(lambda name: ":/fonts/" + name, Fonts.raleway)),
        }


class Sounds:
    # all sounds are free (under Creative Commons Attribution license)
    # downloaded from here -> https://notificationsounds.com/notification-sounds
    sounds = [
        "announcement.wav",
        "chime.wav",
        "concise.wav",
        "delicate-like-sand-paper.wav",
        "gesture.wav",
        "graceful.wav",
        "guess-what.wav",
        "here-it-is.wav",
        "hey-look-at-me.wav",
        "hurry.wav",
        "i-demand-attention.wav",
        "look-this-is-what-i-was-talking-about.wav",
        "losing-patience.wav",
        "oh-finally.wav",
        "oringz-15.wav",
        "oringz-16.wav",
        "scratch.wav",
        "suppressed.wav",
        "this-guitar.wav",
        "youve-been-informed.wav",
    ]

    @staticmethod
    def all() -> dict[str, str]:
        return dict(
            map(
                lambda file: (
                    " ".join(file[:-4].split("-")).title(),  # make name from file name
                    ":/sounds/" + file,  # add location to file name
                ),
                Sounds.sounds,
            )
        )

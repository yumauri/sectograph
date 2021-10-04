import os
import sys
import platform
from PyQt5 import Qt, QtCore, QtWidgets
from sectograph import widgets


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def run() -> None:
    print("Platform:", platform.platform())
    print("Python version:", sys.version.replace("\n", " "))
    print("Qt version:", QtCore.QT_VERSION_STR)
    print("PyQt version:", Qt.PYQT_VERSION_STR)
    sys.excepthook = except_hook

    # make app aware of HiDPI display
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    theme_name = "default"
    app = widgets.Application(sys.argv, theme_name)

    # init windows and widgets
    app.main_window = widgets.MainWindow(app, theme_name)
    app.edit_window = widgets.EditWindow(app, theme_name)
    app.about_window = widgets.AboutWindow(app, theme_name)
    app.tray_widget = widgets.SysTray(app, theme_name)

    # show main window and tray icon
    app.main_window.show()
    app.tray_widget.show()

    sys.exit(app.exec())

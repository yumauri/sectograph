from PyQt5 import QtCore, QtGui, QtWidgets  # , uic
from sectograph import resources, widgets, entities, datetime as dt
from .edit_window_ui import Ui_EditEventForm


repeat = {
    "None": None,
    "Every Day": 1,
    "Every Week": 7,
    "Every 2 Weeks": 14,
    "Every Month": 30,  # actually not a month
    "Every Year": 365,  # actually not a year
}
alert_interval = {
    "None": None,
    "At time of event": 0,
    "5 minutes before": 5,
    "10 minutes before": 10,
    "15 minutes before": 15,
    "30 minutes before": 30,
    "1 hour before": 60,
    "2 hours before": 120,
    "1 day before": 60 * 24,
    "2 days before": 60 * 2 * 24,
}


# class EditWindow(QtWidgets.QWidget):
class EditWindow(QtWidgets.QWidget, Ui_EditEventForm):
    app: widgets.Application
    evt: entities.BaseEvent
    should_play: bool

    def __init__(self, app: widgets.Application, theme_name: str) -> None:
        super().__init__(app.main_window)
        self.app = app
        self.colors = app.colors_repository.get()
        # uic.loadUi('sectograph/widgets/edit_window_ui.ui', self)
        self.setupUi(self)
        self.initUI()

    def initUI(self) -> None:
        self.setWindowFlags(QtCore.Qt.Tool)
        self.installEventFilter(self)

        for i, (name, value) in enumerate(repeat.items()):
            self.repeat_ComboBox.insertItem(i, name)
            self.repeat_ComboBox.setItemData(i, value)

        for color in self.colors:
            self.color_ComboBox.insertItem(1e3, color)

        for i, (name, value) in enumerate(alert_interval.items()):
            self.alert_ComboBox.insertItem(i, name)
            self.alert_ComboBox.setItemData(i, value)

        self.sound_ComboBox.insertItem(0, "None")
        for sound in resources.Sounds.all().keys():
            self.sound_ComboBox.insertItem(1e3, sound)

        self.allday_CheckBox.stateChanged.connect(self.allday_changed)
        self.repeat_ComboBox.currentTextChanged.connect(self.repeat_changed)
        self.endrepeat_ComboBox.currentTextChanged.connect(self.endrepeat_changed)
        self.color_ComboBox.currentTextChanged.connect(self.color_changed)
        self.alert_ComboBox.currentTextChanged.connect(self.alert_changed)
        self.sound_ComboBox.currentTextChanged.connect(self.sound_changed)

        self.save_PushButton.clicked.connect(self.save)
        self.cancel_PushButton.clicked.connect(self.cancel)
        self.delete_PushButton.clicked.connect(self.delete)
        self.sound_PushButton.clicked.connect(self.sound_changed)

    def open_with_new(self):
        # create new empty base event with duration of 15 minutes
        self.open(
            entities.BaseEvent(
                start=dt.app_now(),
                finish=dt.app_now() + dt.timedelta(minutes=15),
                text="",
                color="orange",
            )
        )

    def open(self, evt: entities.BaseEvent):
        self.evt = evt
        self.setWindowTitle(("Edit" if evt.id else "Add") + " event")
        self.text_LineEdit.setText(evt.text)
        self.allday_CheckBox.setChecked(evt.day)
        self.start_DateEdit.setDateTime(evt.start)
        self.finish_DateEdit.setDateTime(evt.finish)
        self.starts_DateTimeEdit.setDateTime(evt.start)
        self.finish_DateTimeEdit.setDateTime(evt.finish)

        # select item in repeat_ComboBox
        self.repeat_ComboBox.setCurrentIndex(list(repeat.values()).index(evt.repeat))

        # select item in endrepeat_ComboBox and end repeat date
        self.endrepeat_ComboBox.setCurrentIndex(0 if evt.end is None else 1)
        if evt.end is not None:
            self.endrepeat_DateEdit.setDateTime(evt.end)

        # select item in color_ComboBox
        if evt.color:
            if evt.color in self.colors:
                self.color_ComboBox.setCurrentIndex(self.colors.index(evt.color))
            else:
                self.color_ComboBox.setEditText(evt.color)

        # select item in alert_ComboBox
        self.alert_ComboBox.setCurrentIndex(
            list(alert_interval.values()).index(evt.notify)
        )

        # select item in sound_ComboBox
        self.should_play = False
        self.sound_ComboBox.setCurrentIndex(
            list(resources.Sounds.all().keys()).index(evt.sound) + 1 if evt.sound else 0
        )

        # actualize form state and show
        self.delete_PushButton.setVisible(not not evt.id)
        self.allday_changed()
        self.repeat_changed()
        self.color_changed()
        self.alert_changed()
        self.sound_changed()
        self.show()

    def allday_changed(self):
        is_day_event = self.allday_CheckBox.isChecked()
        self.starts_DateTimeEdit.setVisible(not is_day_event)
        self.finish_DateTimeEdit.setVisible(not is_day_event)
        self.ends_Label.setVisible(not is_day_event)
        self.start_DateEdit.setVisible(is_day_event)
        self.finish_DateEdit.setVisible(False)
        self.alert_Label.setVisible(not is_day_event)
        self.alert_ComboBox.setVisible(not is_day_event)
        self.alert_changed()

    def repeat_changed(self):
        repeat_idx = self.repeat_ComboBox.currentIndex()
        self.endrepeat_Label.setVisible(repeat_idx != 0)
        self.endrepeat_ComboBox.setVisible(repeat_idx != 0)
        self.endrepeat_changed()

    def endrepeat_changed(self):
        repeat_idx = self.repeat_ComboBox.currentIndex()
        endrepeat_idx = self.endrepeat_ComboBox.currentIndex()
        self.endrepeat_DateEdit.setVisible(repeat_idx != 0 and endrepeat_idx != 0)

    def color_changed(self):
        color = self.color_ComboBox.currentText()
        self.colorshow_Label.setStyleSheet(f"margin-left:5px;background-color:{color}")

    def alert_changed(self):
        alert = self.alert_ComboBox.currentText()
        visible = self.alert_ComboBox.isVisible()
        self.sound_Label.setVisible(visible and alert != "None")
        self.sound_ComboBox.setVisible(visible and alert != "None")
        self.sound_PushButton.setVisible(visible and alert != "None")

    def sound_changed(self):
        name = self.sound_ComboBox.currentText()
        self.sound_PushButton.setDisabled(name == "None")
        if self.sound_ComboBox.isVisible() and self.should_play and name != "None":
            self.app.sound.play(name)
        self.should_play = True

    def cancel(self):
        self.close()

    def save(self):
        # get form data
        text = self.text_LineEdit.text()

        # prevent saving event with empty text
        if not text:
            return

        day = self.allday_CheckBox.isChecked()
        if day:
            start = self.start_DateEdit.date().toPyDate()
            finish = self.finish_DateEdit.date().toPyDate()
            start = dt.datetime.combine(start, dt.app_time())
            finish = dt.datetime.combine(finish, dt.app_time())
        else:
            start = self.starts_DateTimeEdit.dateTime().toPyDateTime()
            finish = self.finish_DateTimeEdit.dateTime().toPyDateTime()
            start = start.replace(second=0, microsecond=0)
            finish = finish.replace(second=0, microsecond=0)
        repeat = self.repeat_ComboBox.itemData(self.repeat_ComboBox.currentIndex())
        if repeat is None or self.endrepeat_ComboBox.currentIndex() == 0:
            end = None
        else:
            end = self.endrepeat_DateEdit.date().toPyDate()
        color = self.color_ComboBox.currentText()
        notify = self.alert_ComboBox.itemData(self.alert_ComboBox.currentIndex())
        notify = notify if self.alert_ComboBox.isVisible() else None
        sound = self.sound_ComboBox.currentText()
        sound = sound if notify is not None and sound != "None" else None

        # compose new event
        evt = entities.BaseEvent(
            id=self.evt.id,
            start=start,
            finish=finish,
            text=text,
            color=color,
            notify=notify,
            sound=sound,
            day=day,
            repeat=repeat,
            end=end,
        )

        # convert to event or day event
        # and update/add this event in database
        if day:
            evt = entities.DayEvent.from_base_event(evt)
            if evt.id:
                self.app.day_events_repository.update(evt)
            else:
                self.app.day_events_repository.add(evt)
        else:
            evt = entities.Event.from_base_event(evt)
            if evt.id:
                self.app.events_repository.update(evt)
            else:
                self.app.events_repository.add(evt)

        # update events and close this window
        self.app.main_window.update_events()
        self.close()

    def delete(self):
        msg_box = QtWidgets.QMessageBox()
        answer = msg_box.question(
            self,
            "Delete event",
            f'Are you sure you want to delete event\n"{self.evt.text}"',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.Yes,
        )

        if answer == QtWidgets.QMessageBox.Yes:
            # delete event
            if self.evt.day:
                self.app.day_events_repository.delete(self.evt)
            else:
                self.app.events_repository.delete(self.evt)

            # update events and close this window
            self.app.main_window.update_events()
            self.close()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if (
                event.key() == QtCore.Qt.Key_Enter
                or event.key() == QtCore.Qt.Key_Return
            ):
                if self.text_LineEdit.text() != "":
                    self.save()
        return super().eventFilter(source, event)

    def showEvent(self, event):
        rect = self.parent().geometry()
        x = rect.x() + rect.width() // 2 - self.width() // 2
        y = rect.y()
        self.move(x, y)
        super().showEvent(event)
        self.activateWindow()

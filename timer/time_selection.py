import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from datetime import datetime
from .types import Position


class TimeSelection(Gtk.Grid):
    calendar: Gtk.Calendar

    spin_hour: Gtk.SpinButton
    spin_minute: Gtk.SpinButton
    spin_second: Gtk.SpinButton

    def __init__(self):
        super().__init__()

        self.setCalendar()
        self.setHours(0)
        self.setMinutes(0)
        self.setSeconds(0)

        self.timeSelectionGrid()

        current_time = datetime.now()
        self.setInitialTime(current_time.hour, current_time.minute, current_time.second)

    def setCalendar(self) -> None:
        self.calendar = Gtk.Calendar()
        self.calendar.set_display_options(
            Gtk.CalendarDisplayOptions.SHOW_DAY_NAMES | Gtk.CalendarDisplayOptions.SHOW_HEADING
        )
        self.calendar.connect("day-selected", self.on_date_selected)

    def setHours(self, hour: int = 0) -> None:
        self.spin_hour = Gtk.SpinButton()
        self.spin_hour.set_range(0, 23)
        self.spin_hour.set_value(hour)

    def setMinutes(self, minute: int = 0) -> None:
        self.spin_minute = Gtk.SpinButton()
        self.spin_minute.set_range(0, 59)
        self.spin_minute.set_increments(1, 5)
        self.spin_minute.set_value(minute)

    def setSeconds(self, second: int = 0) -> None:
        self.spin_second = Gtk.SpinButton()
        self.spin_second.set_range(0, 59)
        self.spin_second.set_increments(1, 5)
        self.spin_second.set_value(second)

    def timeSelectionGrid(self):
        calendar_label_position = Position(0, 0, 1, 1)
        calendar_position = Position(1, 0, 1, 1)
        self.attach(Gtk.Label(label="Select a datetime:"), *calendar_label_position)
        self.attach(self.calendar, *calendar_position)

        hours_label_position = Position(0, 1, 1, 1)
        hours_position = Position(1, 1, 1, 1)
        self.attach(Gtk.Label(label="Hours:"), *hours_label_position)
        self.attach(self.spin_hour, *hours_position)

        minutes_label_position = Position(0, 2, 1, 1)
        minutes_position = Position(1, 2, 1, 1)
        self.attach(Gtk.Label(label="Minutes:"), *minutes_label_position)
        self.attach(self.spin_minute, *minutes_position)

        seconds_label_position = Position(0, 3, 1, 1)
        seconds_position = Position(1, 3, 1, 1)
        self.attach(Gtk.Label(label="Seconds:"), *seconds_label_position)
        self.attach(self.spin_second, *seconds_position)

    def setInitialTime(self, hour, minute, second):
        self.spin_hour.set_value(hour)
        self.spin_minute.set_value(minute)
        self.spin_second.set_value(second)

    def on_date_selected(self, calendar):
        year, month, day = calendar.get_date()

        self.spin_hour.set_value(0)
        self.spin_minute.set_value(0)
        self.spin_second.set_value(0)

    def get_selected_time(self):
        hour = self.spin_hour.get_value_as_int()
        minute = self.spin_minute.get_value_as_int()
        second = self.spin_second.get_value_as_int()
        return hour, minute, second


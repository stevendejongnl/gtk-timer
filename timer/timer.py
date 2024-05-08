import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from datetime import datetime
from .types import Position
from .time_selection import TimeSelection


class Timer(Gtk.Window):
    grid: Gtk.Grid
    time_selection: TimeSelection
    start_button: Gtk.Button
    label_time: Gtk.Label
    timer_id: int
    remaining_time: int

    def setStartButton(self):
        self.start_button = Gtk.Button(label="Start")
        self.start_button.connect("clicked", self.on_start_button_clicked)

    def setTimerLabel(self):
        self.label_time = Gtk.Label(label="00:00:00")

    def setGrid(self):
        self.grid = Gtk.Grid()

        time_selection_position = Position(0, 0, 1, 1)
        self.grid.attach(self.time_selection, *time_selection_position)

        start_button_position = Position(0, 1, 1, 1)
        self.grid.attach(self.start_button, *start_button_position)

        label_time_position = Position(0, 2, 1, 1)
        self.grid.attach(self.label_time, *label_time_position)

        self.add(self.grid)

    def __init__(self):
        Gtk.Window.__init__(self, title="Timer App")

        self.time_selection = TimeSelection()
        self.setStartButton()
        self.setTimerLabel()
        self.setGrid()
        self.timer_id = None
        self.remaining_time = 0

    def on_start_button_clicked(self, button):
        self.start_button.set_sensitive(False)
        hour, minute, second = self.time_selection.get_selected_time()
        self.remaining_time = hour * 3600 + minute * 60 + second
        self.timer_id = GLib.timeout_add_seconds(1, self.update_timer)

    def update_timer(self):
        self.remaining_time -= 1
        hours = self.remaining_time // 3600
        minutes = (self.remaining_time % 3600) // 60
        seconds = self.remaining_time % 60
        self.label_time.set_label("{:02}:{:02}:{:02}".format(hours, minutes, seconds))
        if self.remaining_time <= 0:
            self.label_time.set_label("Time's up!")
            self.present()  # Focus and bring the window to front
            message = "Time's up!", "Your timer has finished."
            self.play_system_sound("complete")
            self.show_notification(*message)
            self.show_popup(*message)
            self.reset_timer()
            return False
        else:
            return True

    def reset_timer(self):
        self.start_button.set_sensitive(True)
        self.time_selection.spin_hour.set_value(0)
        self.time_selection.spin_minute.set_value(0)
        self.time_selection.spin_second.set_value(0)
        self.label_time.set_label("00:00:00")
        if self.timer_id:
            GLib.source_remove(self.timer_id)
            self.timer_id = None

    def play_system_sound(self, sound_name):
        sound_file = f"/usr/share/sounds/freedesktop/stereo/{sound_name}.oga"
        subprocess.Popen(["paplay", sound_file])

    def show_popup(self, title, message):
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.OK, text=title)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def show_notification(self, title, message):
        subprocess.Popen(['notify-send', title, message])

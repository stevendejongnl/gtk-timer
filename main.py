import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class TimeSelection(Gtk.Grid):

    def __init__(self):
        super().__init__()

        # SpinButton for hours
        self.spin_hour = Gtk.SpinButton()
        self.spin_hour.set_range(0, 23)  
        self.spin_hour.set_value(0)      

        # SpinButton for minutes
        self.spin_minute = Gtk.SpinButton()
        self.spin_minute.set_range(0, 59)   
        self.spin_minute.set_increments(1, 5)  
        self.spin_minute.set_value(0)      

        # SpinButton for seconds
        self.spin_second = Gtk.SpinButton()
        self.spin_second.set_range(0, 59)   
        self.spin_second.set_increments(1, 10)  
        self.spin_second.set_value(0)      

        # Grid layout for the widgets
        self.attach(Gtk.Label(label="Hours:"), 0, 0, 1, 1)
        self.attach(self.spin_hour, 1, 0, 1, 1)
        self.attach(Gtk.Label(label="Minutes:"), 0, 1, 1, 1)
        self.attach(self.spin_minute, 1, 1, 1, 1)
        self.attach(Gtk.Label(label="Seconds:"), 0, 2, 1, 1)
        self.attach(self.spin_second, 1, 2, 1, 1)

    def get_selected_time(self):
        hour = self.spin_hour.get_value_as_int()
        minute = self.spin_minute.get_value_as_int()
        second = self.spin_second.get_value_as_int()
        return hour, minute, second

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Timer App")

        # TimeSelection widget
        self.time_selection = TimeSelection()

        # Start button
        self.start_button = Gtk.Button(label="Start")
        self.start_button.connect("clicked", self.on_start_button_clicked)

        # Label to display remaining time
        self.label_time = Gtk.Label(label="00:00:00")

        # Grid layout for the widgets
        self.grid = Gtk.Grid()
        self.grid.attach(self.time_selection, 0, 0, 1, 1)
        self.grid.attach(self.start_button, 0, 1, 1, 1)
        self.grid.attach(self.label_time, 0, 2, 1, 1)

        self.add(self.grid)

        # Timer variables
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
            self.show_notification(*message)
            self.show_popup(*message)
            return False
        else:
            return True

    def show_popup(self, title, message):
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.OK, text=title)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def show_notification(self, title, message):
        subprocess.Popen(['notify-send', title, message])

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

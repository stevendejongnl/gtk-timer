import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from timer.timer import Timer

win = Timer()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

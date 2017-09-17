import os
import subprocess

import gi
gi.require_version('Gedit', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gio, GLib, Gtk, Gedit

from .popup import Popup


class QuickOpenAppActivatable(GObject.Object, Gedit.AppActivatable):
    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.app.add_accelerator("<Primary><Alt>O", "win.quickopen", None)

        self.menu_ext = self.extend_menu("file-section")
        item = Gio.MenuItem.new(_("Quick open..."), "win.quickopen")
        self.menu_ext.prepend_menu_item(item)

    def do_deactivate(self):
        self.app.remove_accelerator("win.quickopen", None)


class QuickOpenPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "QuickOpenPlugin"

    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self._popup_size = (650, 450)
        self._popup = None

        action = Gio.SimpleAction(name="quickopen")
        action.connect('activate', self.on_quick_open_activate)
        self.window.add_action(action)

    def do_deactivate(self):
        self.window.remove_action("quickopen")

    def get_popup_size(self):
        return self._popup_size

    def set_popup_size(self, size):
        self._popup_size = size

    def _create_popup(self):
        paths = []

        doc = self.window.get_active_document()

        # File browser root directory
        bus = self.window.get_message_bus()

        if bus.is_registered('/plugins/filebrowser', 'get_root'):
            msg = bus.send_sync('/plugins/filebrowser', 'get_root')

            if msg:
                gfile = msg.props.location

                if gfile and gfile.is_native():
                    paths.append(gfile)

                    # ... and all subdirectories
                    result = subprocess.run(['find', gfile.get_path(), '-type', 'd'], stdout=subprocess.PIPE)
                    for result_dir in result.stdout.decode('utf-8').split():
                        paths.append(Gio.file_new_for_path(result_dir))

        self._popup = Popup(self.window, paths, self.on_activated)
        self.window.get_group().add_window(self._popup)

        self._popup.set_default_size(*self.get_popup_size())
        self._popup.set_transient_for(self.window)
        self._popup.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self._popup.connect('destroy', self.on_popup_destroy)

    # Callbacks
    def on_quick_open_activate(self, action, parameter, user_data=None):
        if not self._popup:
            self._create_popup()

        self._popup.show()

    def on_popup_destroy(self, popup, user_data=None):
        self.set_popup_size(popup.get_final_size())

        self._popup = None

    def on_activated(self, gfile, user_data=None):
        Gedit.commands_load_location(self.window, gfile, None, -1, -1)
        return True

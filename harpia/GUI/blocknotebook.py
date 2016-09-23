#!/usr/bin/env python
 # -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

from harpia import s2idirectory
from blockstreeview import BlocksTreeView


class BlockNotebook(Gtk.Notebook):

    def __init__(self, main_window):
        Gtk.Notebook.__init__(self)
        self.main_window = main_window
        self.set_scrollable(True)
        # Load blocks
        languages = []
        self.tabs = []
        for x in s2idirectory.block:
            if s2idirectory.block[x].language in languages:
                continue
            languages.append(s2idirectory.block[x].language)
        for language in languages:
            treeview = BlocksTreeView(self.main_window, language)
            self.append_page(treeview, Gtk.Label(language))
            self.tabs.append(treeview)

    # ----------------------------------------------------------------------
    def get_current_tab(self):
        if self.get_current_page() > -1:
            return self.tabs[self.get_current_page()]
        else:
            return None

    # ----------------------------------------------------------------------
    def get_tabs(self):
        return self.tabs
# ----------------------------------------------------------------------            
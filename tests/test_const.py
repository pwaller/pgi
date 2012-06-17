# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import unittest


class ConstTest(unittest.TestCase):
    def test_int(self):
        self.assertEqual(Gtk.MAJOR_VERSION, 3)
        self.assertEqual(Gtk.PRIORITY_RESIZE, 10)
        self.assertEqual(Gtk.INPUT_ERROR, -1)

    def test_string(self):
        self.assertEqual(Gtk.STYLE_CLASS_SCALE, 'scale')
        self.assertEqual(Gtk.PRINT_SETTINGS_PRINTER, 'printer')
        self.assertEqual(Gtk.STOCK_ABOUT, 'gtk-about')
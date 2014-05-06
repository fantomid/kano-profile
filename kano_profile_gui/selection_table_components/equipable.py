#!/usr/bin/env python

# equipable.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# This controls the size and styling of the pictures displayed on the table
# Used for badges, environments and avatar screen


from gi.repository import Gtk
import individual_item as indiv_item


class Equipable(indiv_item.IndividualItem):
    def __init__(self, info):
        # info is a dictionary containing name of picture file, heading, date, info about the item, hover over text shown
        indiv_item.IndividualItem.__init__(self, info)

        # Event box containing the time and title of the equipped item
        self.equipped_box = Gtk.EventBox()
        self.equipped_box.get_style_context().add_class("equipped_box")
        self.equipped_box.set_visible_window(False)
        self.equipped_label = Gtk.Label(self.title)
        self.equipped_box.add(self.equipped_label)
        self.equipped_box.set_size_request(self.width, self.label_height)

        # Event box containing the EQUIPPED label
        self.equipped_label2 = Gtk.Label("EQUIPPED")
        self.equipped_box2 = Gtk.EventBox()
        self.equipped_box2.get_style_context().add_class("equipped_box2")
        self.equipped_box2.add(self.equipped_label2)
        self.equipped_box2.set_size_request(115, 30)

        # Border box of equipped style
        self.equipped_border = Gtk.EventBox()
        self.equipped_border.get_style_context().add_class("equipped_border")
        self.equipped_border.set_size_request(125, 40)

        self.fixed.put(self.equipped_box, 0, self.height - self.label_height)
        self.fixed.put(self.equipped_border, 10, 10)
        self.fixed.put(self.equipped_box2, 15, 15)

        # Default, set equipped to False.
        self.equipped = False

        # Items can be equipped
        self.equipable = True

    # Sets whether the picture is equipped
    # equipped = True or False
    def set_equipped(self, equipped):
        self.equipped = equipped

    def get_equipped(self):
        return self.equipped

    def toggle_equipped(self, arg1=None, arg2=None):
        self.set_equipped(not self.get_equipped())

    # This function contains the styling applied to the picture when it is equipped.
    def add_equipped_style(self, arg1=None, arg2=None):
        self.equipped_box.set_visible_window(True)
        self.equipped_label.set_visible(True)
        self.equipped_box2.set_visible_window(True)
        self.equipped_label2.set_visible(True)
        self.equipped_border.set_visible_window(True)

    def remove_equipped_style(self, arg1=None, arg2=None):
        self.equipped_box.set_visible_window(False)
        self.equipped_label.set_visible(False)
        self.equipped_box2.set_visible_window(False)
        self.equipped_label2.set_visible(False)
        self.hover_box.set_visible_window(False)
        self.hover_label.set_visible(False)
        self.equipped_border.set_visible_window(False)

#!/usr/bin/env python

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# table_template.py
#
# Controls interaction between table and info screen

from gi.repository import Gtk
import kano_profile_gui.selection_table_components.table_ui as tab
import kano_profile_gui.selection_table_components.info_screen_ui as info_screen
import kano_profile_gui.components.header as header


# headers: category names, e.g. ["badges"] or ["environments"]
# equipable: whether each item in the array is equipable (like avatars or environments)
class TableTemplate():
    def __init__(self, headers, equipable):

        self.equipable = equipable
        self.scrollbar_width = 44
        self.width = 734 - self.scrollbar_width
        self.height = 448

        self.categories = []
        for x in range(len(headers)):
            self.categories.append(tab.TableUi(headers[x], self.equipable))

        if len(headers) == 2:
            self.head = header.Header(headers[0], headers[1])
            self.head.set_event_listener1(self.on_button_toggled)
        else:
            self.head = header.Header(headers[0])

        for cat in self.categories:
            for pic in cat.pics:
                pic.button.connect("button_press_event", self.go_to_info_screen, pic, cat)

        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.add_with_viewport(self.categories[0].grid)
        self.scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolledwindow.set_size_request(self.width, self.height)

        self.container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.container.pack_start(self.head.box, False, False, 0)
        self.container.pack_start(self.scrolledwindow, False, False, 0)

        # Set the equipped items based on what we read from file

        # Read from file here
        self.equip_with_tuple("environments", "all", "fields_of_ideas")
        self.equip_with_tuple("avatars", "gumps", "gumps_2")

    def on_button_toggled(self, button):
        in_cat1 = button.get_active()
        for cat in self.categories:
            container = cat.grid.get_parent()
            if container is not None:
                container.remove(cat.grid)
        for i in self.scrolledwindow.get_children():
            self.scrolledwindow.remove(i)
        if in_cat1:
            self.scrolledwindow.add_with_viewport(self.categories[0].grid)
        else:
            self.scrolledwindow.add_with_viewport(self.categories[1].grid)
        self.scrolledwindow.show_all()
        self.hide_labels()

    def go_to_info_screen(self, arg1=None, arg2=None, pic=None, cat=None):
        selected_item_screen = info_screen.InfoScreenUi(pic.items)
        for i in self.container.get_children():
            self.container.remove(i)
        self.container.add(selected_item_screen.container)
        selected_item_screen.info_text.back_button.connect("button_press_event", self.leave_info_screen)
        if self.equipable:
            # This doesn't work because we're not changing the selected_item
            # We need to set a flag or self.selected = True
            # selected_item_screen.info.equip_button.connect("button_press_event", self.equip, cat, selected_item)
            selected_item_screen.info_text.equip_button.connect("button_press_event", self.equip, pic, cat)
        self.container.show_all()

        # Remove locked images from selected item screen
        #selected_item_screen.set_locked()

    def equip(self, arg1=None, arg2=None, pic=None, cat=None):
        cat.unequip_all()
        pic.set_equipped_item()
        self.leave_info_screen()
        print cat.get_equipped_tuple()

    def leave_info_screen(self, arg1=None, arg2=None):
        for i in self.container.get_children():
            self.container.remove(i)
        self.container.pack_start(self.head.box, False, False, 0)
        self.container.pack_start(self.scrolledwindow, False, False, 0)
        self.container.show_all()
        # Hide all labels on images
        self.hide_labels()

    def hide_labels(self):
        for cat in self.categories:
            cat.hide_labels()

    def equip_with_tuple(self, category, subcategory, name):
        for cat in self.categories:
            for pic in cat.pics:
                item = pic.items.get_item_from_tuple(category, subcategory, name)
                if item is not None:
                    pic.items.set_visible_item(item)
                    self.equip(None, None, pic, cat)

    def get_equipped_tuple(self):
        for i in range(2):
            print self.headers[i], self.categories[i].get_equipped_tuple()


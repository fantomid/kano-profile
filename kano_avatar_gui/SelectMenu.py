#!/usr/bin/env python

# SelectMenu.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk
from kano.gtk3.apply_styles import apply_styling_to_screen
from kano_avatar.paths import CSS_PATH
from kano.logging import logger


# TODO: try and replace the current structure with the parser?
# the selected functions would then be redundant
# However, the parser doesn't have a selected category section, so it may not
# work for the selcted categories.
class SelectMenu(Gtk.EventBox):
    def __init__(self, list_of_names, signal_name):

        Gtk.EventBox.__init__(self)
        apply_styling_to_screen(CSS_PATH)

        # Initialise self._items
        self._set_items(list_of_names)

        self._signal_name = signal_name

        # This is the selected_identifier
        self._selected = None
        self.get_style_context().add_class('select_menu')

    def _set_items(self, list_of_names):
        self._items = {}

        for name in list_of_names:
            self._items[name] = {}
            self._items[name]['selected'] = False

    def set_selected(self, identifier):
        '''Sets the selected element in the dictionary to True,
        and sets all the others to False
        '''

        self._selected = identifier

    def get_selected(self):
        '''Gets the name of the current selected image
        '''

        return self._selected

    def _unselect_all(self):
        '''Remove all styling on all images, and sets the 'selected'
        field to False
        '''
        self._selected = None

    def _add_option_to_items(self, identifier, name, item):
        '''Adds a new option in the self._items
        '''
        if identifier in self._items:
            self._items[identifier][name] = item

    def _remove_option_from_items(self, identifier, name):
        if identifier in self._items:
            self._items[identifier].pop(name, None)

    def get_option(self, identifier, option):
        if identifier in self._items:
            if option in self._items[identifier]:
                return self._items[identifier][option]

        return None

    def set_button(self, identifier, button):
        if identifier in self._items:
            self._items[identifier]['button'] = button
        else:
            logger.error(
                "Trying to set a button for an identifier that is not present")

    def unset_button(self, identifier):
        self._remove_option_from_items(identifier, 'button')

    def get_button(self, identifier):
        if identifier in self._items:
            if 'button' in self._items[identifier]:
                return self._items[identifier]['button']

        logger.error(
            "Trying to get a button for an identifier that is not present")
        return None

    def _add_selected_css(self, button):
        style = button.get_style_context()
        style.add_class('selected')

    def _remove_selected_css(self, button):
        style = button.get_style_context()
        style.remove_class('selected')

    def _add_selected_image(self, button, identifier):
        '''Pack the selected image into the button
        '''
        if 'active_path' in self._items[identifier]:
            path = self._items[identifier]['active_path']
            image = Gtk.Image.new_from_file(path)
            button.set_image(image)

    def _remove_selected_image(self, button, identifier):
        '''Pack the grey unselected image into the button
        '''
        if 'inactive_path' in self._items[identifier]:
            path = self._items[identifier]['inactive_path']
            image = Gtk.Image.new_from_file(path)
            button.set_image(image)

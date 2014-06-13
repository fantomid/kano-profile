#!/usr/bin/env python

# badges.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#


import kano_profile_gui.selection_table_components.table_template as table_template

badge_ui = None


def activate(_win, _box):
    global badge_ui

    headers = ["badges"]
    equipable = False

    # So we don't overwrite the current selected items
    # If we read and write to a config file, this isn't needed
    if badge_ui is None:
        badge_ui = table_template.TableTemplate(headers, equipable)

    # Leave the info screen
    badge_ui.leave_info_screen()
    _box.pack_start(badge_ui.container, False, False, 0)

    _win.show_all()

    badge_ui.hide_labels()

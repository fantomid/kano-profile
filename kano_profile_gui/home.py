#!/usr/bin/env python

# home.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from gi.repository import Gtk
from kano.profile.profile import load_profile
from kano.profile.badges import calculate_xp, calculate_kano_level

import kano_profile_gui.home_components.home_stats as home_stats
import kano_profile_gui.home_components.home_picture as home_pic


def activate(_win, _box):
    #_label.set_text('Home')
    image_width = 734
    image_height = 404

    profile = load_profile()

    xp = calculate_xp()
    level, progress = calculate_kano_level()
    name = profile['username_linux']

    # Picture box - contains image depends on level reached
    picture_box = Gtk.Box()
    picture = home_pic.Picture().fixed
    picture_box.add(picture)
    picture_box.set_size_request(image_width, image_height)

    # Stats
    stat_dict = {"Name": name, "XP": xp, "Level": level, "Progress": progress}
    stats = home_stats.Stats(_win.WINDOW_WIDTH, stat_dict)

    _box.pack_start(picture_box, False, False, 0)
    _box.pack_start(stats.container, False, False, 0)

    #msg = 'name: {}\nXP: {}\nLevel: {}\nProgress to next level: {:.0%}'.format(name, xp, level, progress)

    #label = Gtk.Label()
    #label.set_text(msg)
    #_box.add(label)

    _win.show_all()



# quests.py
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

import os
import json
import imp
import 

from kano.logging import logger
from kano.utils import read_json, is_gui, is_running, run_bg
from .paths import xp_file, levels_file, rules_dir, bin_dir, \
    app_profiles_file, online_badges_dir, online_badges_file
from .apps import load_app_state, get_app_list, save_app_state


QUESTS_LOAD_PATH = "/usr/share/kano-profile/quests"

class Quests(object):
    """
        Manages quest modules.

        It loads them up from different locations and constructs an
        instance for each quest.
    """

    def __init__(self):
        self._quests = []

    def _load_system_modules(self):
        module_files = []
        for f in os.listdir(QUESTS_LOAD_PATH):
            full_path = os.path.join(QUESTS_LOAD_PATH, f)
            modname = os.path.basename(f)
            if os.path.isfile(full_path):
                qmod = imp.load_source(modname, full_path)
                self._quests.append(qmod.init())


    def _load_external_modules(self):
        """
            TODO: This needs to be populated from kano-content
        """
        pass

    def list_quests(self):
        return self._quests

    def list_active_quests(self):
        """
            Active quest is one that should be displayed in the UI and that
            can be worked on by the user.

            Currently, active quests are those ones that have all their
            dependencies completed, but haven't been completed themselves.
        """
        active = []
        for quest in self._quests:
            if quest.is_active:
                active.append(quest)

        return active

    def get_quest(name):
        pass

    def evaluate_xp(self):
        xp = 0
        for quest in self._quests:
            if quest.is_completed():
                xp += quest.get_xp()

        return xp

    def evaluate_badges(self):
        badges = []
        for quest in self._quests:
            if quest.is_completed():
                badges += quest.get_badges()

        return badges


class Step(object):
    """
        Represents one step towards completing a quest.

        This is just a base class. Needs to be implemented by the quest.
    """

    def __init__(self):
        self._title = None
        self._help = None

    def is_completed(self):
        pass


class Quest(object):
    """
        A base class for each quest.
    """

    def __init__(self, manager):
        self._manager = manager
        self._name = None
        self._title = None
        self._description = None
        self._steps = []
        self._xp = 0
        self._badges = []
        self._depends = []

    def is_completed(self):
        completed = True
        for step in self._steps:
            completed = completed and step.is_completed()
        return completed

    def is_active(self):
        active = True
        for dep_name in self._depends:
            quest = self._manager.get_quest(dep_name)
            active = active and quest.is_completed()
        return active

    def get_xp(self):
        return self._xp

    def get_badges(self):
        return self._badges

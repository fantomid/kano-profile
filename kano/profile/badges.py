#!/usr/bin/env python

# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from __future__ import division

import os

from ..utils import read_json, is_gui, run_cmd
from .paths import xp_file, levels_file, rules_dir, bin_dir
from .apps import load_app_state, get_app_list, save_app_state
from .profile import is_unlocked


def calculate_xp():
    allrules = read_json(xp_file)
    if not allrules:
        return -1

    points = 0

    for app, groups in allrules.iteritems():
        appstate = load_app_state(app)
        if not appstate:
            continue

        for group, rules in groups.iteritems():
            # calculating points based on level
            if group == 'level' and 'level' in appstate:
                maxlevel = int(appstate['level'])

                for level, value in rules.iteritems():
                    level = int(level)
                    value = int(value)

                    if level <= maxlevel:
                        points += value

            # calculating points based on multipliers
            if group == 'multipliers':
                for thing, value in rules.iteritems():
                    value = float(value)
                    if thing in appstate:
                        points += value * appstate[thing]

    return int(points)


def calculate_kano_level():
    level_rules = read_json(levels_file)
    if not level_rules:
        return -1, 0

    max_level = max([int(n) for n in level_rules.keys()])
    xp_now = calculate_xp()

    for level in xrange(1, max_level + 1):
        level_min = level_rules[str(level)]

        if level != max_level:
            level_max = level_rules[str(level + 1)] - 1
        else:
            level_max = float("inf")

        if level_min <= xp_now <= level_max:
            reached_level = level
            reached_percentage = (xp_now - level_min) / (level_max + 1 - level_min)

            return int(reached_level), reached_percentage


def calculate_badges():

    # helper function to calculate operations
    def do_calculate(select_push_back):
        for category, subcats in all_rules.iteritems():
            for subcat, items in subcats.iteritems():
                for item, rules in items.iteritems():
                    target_pushback = 'push_back' in rules and rules['push_back'] is True
                    if target_pushback != select_push_back:
                        continue

                    if rules['operation'] == 'stat_gta':
                        achieved = True
                        for target in rules['targets']:
                            app = target[0]
                            variable = target[1]
                            value = target[2]

                            if app not in app_list or variable not in app_state[app]:
                                achieved = False
                                break
                            achieved &= app_state[app][variable] >= value

                    elif rules['operation'] == 'stat_sum_gt':
                        sum = 0
                        for target in rules['targets']:
                            app = target[0]
                            variable = target[1]

                            if app not in app_list or variable not in app_state[app]:
                                continue

                            sum += float(app_state[app][variable])

                        achieved = sum >= rules['value']

                    else:
                        print 'unknown uperation {}'.format(rules['operation'])
                        continue

                    calculated_badges.setdefault(category, dict()).setdefault(subcat, dict())[item] \
                        = all_rules[category][subcat][item]
                    calculated_badges[category][subcat][item]['achieved'] = achieved

    def count_offline_badges():
        return 18

        # TODO implement proper count
        # count = 0
        # for category, items in badges.iteritems():
        #     for item, value in items.iteritems():
        #         if value:
        #             count += 1
        # return count

    app_list = get_app_list() + ['kano-world']
    app_state = dict()
    for app in app_list:
        app_state[app] = load_app_state(app)

    # special app: kanoprofile
    profile_state = dict()
    profile_state['xp'] = calculate_xp()
    profile_state['level'], _ = calculate_kano_level()
    app_state['kano-world'] = profile_state

    all_rules = load_badge_rules()
    calculated_badges = dict()

    # normal ones
    do_calculate(False)

    # count offline badges
    app_state['kano-world']['num_offline_badges'] = count_offline_badges()

    # add pushed back ones
    do_calculate(True)

    return calculated_badges


def compare_badges_dict(old, new):
    if old == new:
        return []
    changes = dict()

    for category, subcats in new.iteritems():
        for subcat, items in subcats.iteritems():
            for item, rules in items.iteritems():
                try:
                    if old[category][subcat][item]['achieved'] is False and \
                       new[category][subcat][item]['achieved'] is True:
                        changes.setdefault(category, dict()).setdefault(subcat, dict())[item] \
                            = new[category][subcat][item]
                except Exception:
                    pass
    return changes


def save_app_state_with_dialog(app_name, data):
    old_level, _ = calculate_kano_level()
    old_badges = calculate_badges()

    save_app_state(app_name, data)

    new_level, _ = calculate_kano_level()
    new_badges = calculate_badges()

    # new level
    new_level_str = ''
    if old_level != new_level:
        new_level_str = 'level:{}'.format(new_level)

    # new items
    new_items_str = ''
    badge_changes = compare_badges_dict(old_badges, new_badges)
    if badge_changes:
        for category, subcats in badge_changes.iteritems():
            for subcat, items in subcats.iteritems():
                for item, rules in items.iteritems():
                    new_items_str += ' {}:{}:{}'.format(category, subcat, item)

    if not new_level_str and not new_items_str:
        return

    if is_gui():
        cmd = '{bin_dir}/kano-profile-levelup {new_level_str} {new_items_str}' \
            .format(bin_dir=bin_dir, new_level_str=new_level_str, new_items_str=new_items_str)
        # TODO remove print
        print run_cmd(cmd)[0]


def save_app_state_variable_with_dialog(app_name, variable, value):
    if is_unlocked() and variable == 'level':
        return
    data = load_app_state(app_name)
    data[variable] = value
    save_app_state_with_dialog(app_name, data)


def increment_app_state_variable_with_dialog(app_name, variable, value):
    if is_unlocked() and variable == 'level':
        return
    data = load_app_state(app_name)
    if variable not in data:
        data[variable] = 0
    data[variable] += value
    save_app_state_with_dialog(app_name, data)


def load_badge_rules():
    if not os.path.exists(rules_dir):
        print 'rules dir missing'
        return

    merged_rules = dict()
    subfolders = ['avatars', 'badges', 'environments']
    for folder in subfolders:
        folder_fullpath = os.path.join(rules_dir, folder)
        if not os.path.exists(folder_fullpath):
            print 'rules subfolder missing: {}'.format(folder_fullpath)
            return

        rule_files = os.listdir(folder_fullpath)
        if not rule_files:
            print 'no rule files in subfolder: {}'.format(folder_fullpath)
            return

        for rule_file in rule_files:
            rule_file_fullpath = os.path.join(folder_fullpath, rule_file)
            rule_data = read_json(rule_file_fullpath)
            if not rule_data:
                print 'rule file empty: {}'.format(rule_file_fullpath)
                continue

            category = folder
            subcategory = rule_file.split('.')[0]

            merged_rules.setdefault(category, dict())[subcategory] = rule_data
    return merged_rules


#
# tracking_sessions.py
#
# Copyright (C) 2014 - 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Functions for tracking app session times
#


import os
import json
import time
from uuid import uuid1, uuid5

from kano.utils.hardware import get_cpu_id
from kano.utils.file_operations import read_file_contents, chown_path
from kano.logging import logger
from kano_profile.tracker.tracker_token import TOKEN
from kano_profile.paths import tracker_dir, tracker_events_file
from kano_profile.tracker.tracking_utils import open_locked, get_utc_offset


OS_VERSION = str(read_file_contents('/etc/kanux_version'))
os_variant = read_file_contents('/etc/kanux_version_variant')
OS_VERSION += '-' + os_variant if os_variant else ''
CPU_ID = str(get_cpu_id())
LANGUAGE = (os.getenv('LANG') or '').split('.', 1)[0]


def get_session_file_path(name, pid):
    return "{}/{}-{}.json".format(tracker_dir, pid, name)


def get_session_unique_id(name, pid):
    data = {}
    tracker_session_file = get_session_file_path(name, pid)
    try:
        af = open_locked(tracker_session_file, 'r')
    except (IOError, OSError) as e:
        logger.error("Error while opening session file".format(e))
    else:
        with af:
            try:
                data = json.load(af)
            except ValueError as e:
                logger.error("Session file is not a valid JSON")

    return data.get('app_session_id', "")


def session_start(name, pid=None):
    if not pid:
        pid = os.getpid()
    pid = int(pid)

    data = {
        'pid': pid,
        'name': name,
        'started': int(time.time()),
        'elapsed': 0,
        'app_session_id': str(uuid5(uuid1(), name + str(pid))),
        'finished': False,
        'token-system': TOKEN
    }

    path = get_session_file_path(data['name'], data['pid'])

    try:
        f = open_locked(path, 'w')
    except IOError as e:
        logger.error("Error opening tracker session file {}".format(e))
    else:
        with f:
            json.dump(data, f)
        if 'SUDO_USER' in os.environ:
            chown_path(path)

    return path


def session_end(session_file):
    if not os.path.exists(session_file):
        msg = "Someone removed the tracker file, the runtime of this " \
              "app will not be logged"
        logger.warn(msg)
        return

    try:
        rf = open_locked(session_file, 'r')
    except IOError as e:
        logger.error("Error opening the tracker session file {}".format(e))
    else:
        with rf:
            data = json.load(rf)

            data['elapsed'] = int(time.time()) - data['started']
            data['finished'] = True

            try:
                wf = open(session_file, 'w')
            except IOError as e:
                logger.error(
                    "Error opening the tracker session file {}".format(e))
            else:
                with wf:
                    json.dump(data, wf)
        if 'SUDO_USER' in os.environ:
            chown_path(session_file)


def get_session_event(session):
    """ Construct the event data structure for a session. """

    return {
        'type': 'session',
        'time': session['started'],
        'timezone_offset': get_utc_offset(),
        'os_version': OS_VERSION,
        'cpu_id': CPU_ID,
        'token': TOKEN,
        'language': LANGUAGE,
        'name': session['name'],
        'length': session['elapsed'],
        'token-system': session.get('token-system', '')
    }


def session_log(name, started, length):
    """ Log a session that was tracked outside of the tracker.

        :param name: The identifier of the session.
        :type name: str

        :param started: When was the session started (UTC unix timestamp).
        :type started: int

        :param length: Length of the session in seconds.
        :param started: int
    """

    try:
        af = open_locked(tracker_events_file, 'a')
    except IOError as e:
        logger.error("Error while opening events file".format(e))
    else:
        with af:
            session = {
                'name': name,
                'started': int(started),
                'elapsed': int(length)
            }

            event = get_session_event(session)
            af.write(json.dumps(event) + "\n")
        if 'SUDO_USER' in os.environ:
            chown_path(tracker_events_file)
#!/usr/bin/env python

# activate_account.py
# 
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
#

import sys
import os
import requests

if __name__ == '__main__' and __package__ is None:
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if dir_path != '/usr':
        sys.path.insert(1, dir_path)


from kano_world.connection import api_url


if len(sys.argv) != 2:
    sys.exit('Wrong usage, needs to supply code')
else:
    code = sys.argv[1]

r = requests.post(api_url + '/accounts/activate/' + code)

print r.text

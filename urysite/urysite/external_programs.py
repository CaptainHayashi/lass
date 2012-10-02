"""Interfacing code for conversing with external URY programs."""

import json
import subprocess


def run_dbpassget(password_key):
    """Runs the URY database password tool, asking for the given
    password key.

    This will only work if django is being run as a user that has
    access to that password.

    """
    # For more information on how dbpassget works and how to maintain
    # it, check the wiki
    dbstanza = subprocess.check_output(
        'echo "{0}" | /usr/local/bin/dbpassget-django'.format(
            password_key.translate(None, '"')),
            shell=True)

    # Output should be "OK <json encoding of Python dictionary>".
    condition, sep, dbconfig = dbstanza.partition(' ')
    if (condition != 'OK'):
        raise ValueError(
            "dbpassget isn't working, returned: {0}".format(dbstanza))
    return json.loads(dbconfig)
    # End magick.  If you didn't understand this, blame Matt Windsor,
    # dbpassget is his abomination.

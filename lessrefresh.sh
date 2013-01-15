#!/bin/sh

# Quick wrapper for updating LESS

touch /usr/local/urysite/static/less/main.less
./manage.py collectstatic --noinput

#!/bin/sh

# Quick wrapper for updating LESS

touch urysite/static/less/main.less
./manage.py collectstatic --noinput

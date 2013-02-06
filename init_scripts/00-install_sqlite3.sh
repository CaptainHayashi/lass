#!/bin/sh

VENV=$VIRTUAL_ENV

mkdir -p $VENV/packages && cd $VENV/packages
wget -N http://www.sqlite.org/sqlite-autoconf-3071401.tar.gz
tar xzvf sqlite-autoconf-3071401.tar.gz

cd $VENV/packages/sqlite-autoconf-3071401
./configure --prefix=$VENV && make && make install

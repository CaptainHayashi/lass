========================
Installation Information
========================

Required Data
=============

You will need to populate the database with some initial data. Where
possible, the data is provided as fixtures to load with Django's
``loaddata`` command.


Filler show
-----------

The filler show must be created in order to allow the schedule
filling algorithms to work properly.

The provided ``schedules/fixtures/filler_show.json`` fixture gives
an example configuration for the filler show.  Note that this
fixture is incomplete: it does not *approve* or assign a *creator*
to the show location, and the primary keys will likely need to be
adjusted.

In addition, ``filler_show.json`` does *not* contain show metadata;
you will need to add that manually for the time being.

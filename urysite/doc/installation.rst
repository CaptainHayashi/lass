.. _installation:

========================
Installation Information
========================

.. sectionauthor:: Matt Windsor <matt.windsor@ury.org.uk>

`LASS` is a non-trivial project to install.  Work is constantly being
carried out to make the project easier to deploy, but at this early
stage installation requires a large amount of manual intervention.

Prerequisite Modules
====================

At the time of writing, `LASS` requires a large amount of Django apps
to be installed manually.  Check the `urysite.contrib_apps` module
for hints as to what you will need.

Templates and Static Files
==========================

The `LASS` distribution does *not* include templates; these will
eventually be available from the same locations as the code
distribution, or you can roll your own if you choose.

Similarly, static files (CSS, images etc.) are not provided - you will
almost certainly want to make your own statics as the ones used at URY
constitute URY's unique station branding.

A "vanilla" set of CSS/LESS stylesheets may be provided in the future.

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

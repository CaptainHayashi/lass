====
LASS
====

**This code is no longer in use at URY and usage is strongly discouraged.  See "lass-pyramid" instead.**

This repository contains the core of the University Radio York
website, the `Longevity Assured Site System`.  It is written in Python
2.7 using the Django 1.4+ framework, and is licenced under the terms
of the GNU General Public Licence version 2.

At time of writing the code is heavily coupled to its original
intended use as the URY website (but with URY branding elements and
private configuration data stripped out), but work is ongoing to make
this codebase generalisable to any student radio station.

Why is this here?
=================

For a few reasons, really:

1) The site is built on *many* existing free software apps and
   frameworks, and giving back to the same community is only fair;
2) It is idealistically hoped that the codebase will eventually be
   generalisable to other student, amateur and local radio stations;
3) It gives prospective URY members something concrete to look at
   before considering whether to join our computing team;
4) It improves the chances of any malpractices or security violations
   in our front-facing code are found and highlighted =P

How do I install this?
======================

(This section to be filled out better later)

The ``requirements.txt`` file can be used to drag in all of LASS's
dependencies, including the most recent checkout of the LASS github,
using ``pip install -r requirements.txt``.

Deploy as a WSGI application; you will need to fill in the Django
settings that `lass/urysite/settings.py` attempts to load from
elsewhere; example private configuration can be found in
`lass/examples`.

Where are the templates?
========================

The templates as used on the URY site are (or will be) on github under
the name `urysite-templates`.

Where are the static files? (CSS, images etc.)
==============================================

These are considered part of URY's branding and thus are not available
from github.  You may find them in processed form on the URY website,
but generally you must ask for permission to use our branding assets.

Where can I find real documentation?
====================================

Sphinx documentation is provided (in the urysite/doc directory).  For
now, this is the only documentation provided.

You're violating my licence!
============================

Please contact us at computing@ury.org.uk if you think that this code
is violating the terms of any licence, and we'll try our hardest to
rectify the problems.

Future directions
=================

1) Clean up the code and make it more presentable for public appraisal
2) Remove specific references to URY
3) Improve this documentation
4) Possibly host the Sphinx documentation on readthedocs when the
   project is more publicly approachable

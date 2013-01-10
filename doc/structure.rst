.. _structure:

============================
Structure of the LASS system
============================

.. sectionauthor:: Matt Windsor<matt.windsor@ury.org.uk>

This is a brief overview of the structure of the *LASS* project as a
whole, including its sub-apps.

In cases where the current state of the code differs from this
outline, the code takes precedence.  LASS is a constantly changing
beast, and thus this can go out of date very quickly.

Why is there so much boilerplate/wheel reinventing?
===================================================

Often, LASS has needed to reinvent things that Django or existing
applications already do.

The usual reason for this is that it is very important that LASS's
database usage plays fair with existing URY applications both legacy
and new, and thus the tendency is to eschew any system that would
introduce "djangoisms" into the database.  This includes things like
content-types, MySQL-style prefixed tables (URY runs PostgreSQL), as
well as the desire for LASS to be able to use URY's database table
naming conventions where possible.

Usually when it comes to things that LASS doesn't need to share with
other applications, our main philosophy is to reuse where possible,
which is why LASS pulls in a large amount of external apps at the
website level.

Another reason is that we're only human, and genuinely might have
overlooked a better solution!

Base modules
============

Most of LASS is implemented in a few highly generalised apps, which
provide a class framework for the higher levels of the system to use.

These are referred to here, with documentation links, in a vague order
from low-level to high-level.  Usually items referenced lower down the
list will have dependencies on packages higher up.

Utils
-----

The "root" of the system is the ``django-lass-utils`` app, which is
intended to have no other dependencies from the LASS project.

The utils app contains a large amount of extremely general mixins and
other features used by practically everything else, including:

* The ``AttachableMixin`` pattern for quickly creating models that
  provide extra data to other models, in a manner that doesn't pollute
  the database with Django-specific idioms;
* The ``Type`` abstract model, used for anything that refers to a type
  or category of other model (for example, show types; metadata keys) 
* Various other odds and ends.

The documentation for ``django-lass-utils`` is
`here <http://django-lass-utils.rtfd.org>`_.

People
------

Large amounts of data in LASS are tied to people, for example show
credits, data change approval, metadata creators and so on.  The
``django-lass-people`` app provides mixins, models and other items for
dealing with these.

The documentation for ``django-lass-people`` is
`here <http://django-lass-people.rtfd.org>`_.

Metadata
--------

A large part of the LASS backbone is the ``django-lass-metadata`` app,
which implements a general metadata system using the
``AttachableMixin`` from ``django-lass-utils`` that can be used to
attach typed key-value metadata (with history and both single and
multiple-value support) to arbitrary models.

It also provides, through ``MetadataSubjectMixin``, a very simple API
for accessing metadata that has been attached to models.  Often,
currently valid metadata can be accessed as if it was an attribute on
the model, making transition to and from the metadata system easy.

LASS uses this nearly everywhere where items of data need titles,
descriptions, tags, attached images, or internal notes.

The documentation for ``django-lass-metadata`` is
`here <http://django-lass-metadata.rtfd.org>`_.

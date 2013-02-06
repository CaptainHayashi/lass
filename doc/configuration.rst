.. _configuration:

=============
Configuration
=============

.. sectionauthor:: Matt Windsor<matt.windsor@ury.org.uk>

*LASS* uses the Django configuration system, but in a slightly
customised manner using YAML files for most of the configuration
options.

Some config is still baked into the *settings.py* file; usually this
is either things that cannot be expressed well in YAML, things that
should be common to all LASS installations, and also the bootstrap
for the YAML configuration system.

Configuration files
===================

You will generally need to supply some Django settings to LASS before
it works, most notably the database and assets locations.  These use
the standard Django names (``DATABASES``, ``TEMPLATE_DIRS`` etc), but
are read from YAML files (ending in '.yml') in the ``private``
directory.  (The name is an artefact from its use to store URY-private
settings.)

LASS loads all ``*.yml`` files in Python string sort order, with each
settings file clobbering any previous Django settings loaded.  This
means that you can store site and server-specific settings in files
named such as to come after more general settings files, and indeed
this is how URY resolve differences between environments.

File format
-----------

Each file should contain a map of Django values to the YAML
representations of their settings, as interpreted by *PyYAML*.  An
example::

    # This can be overridden by YAML files loaded later
    DEBUG: False
     
    # Paths
    MEDIA_ROOT: /usr/local/assets/media
    STATIC_ROOT: /usr/local/assets/static

    # Admins
    ADMINS:
        - - Head of Everything
          - hoe@radio.example.com
        - - Webmaster
          - sucker@radio.example.com
    SERVER_EMAIL: noreply@example.com

Files can obviously contain any YAML syntax that *PyYAML* understands.

Defaults
--------

Some Django settings have default values baked into ``settings.py`` in
the event that they are not specified in any private YAML.  See the
code file for information.

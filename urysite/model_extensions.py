"""URY extensions to/shortcuts for the Django model system.

"""

from django.db import models


def primary_key(db_column):
    """Shorthand for Django's AutoField-primary-key idiom.

    URY's database consistency guidelines are in conflict with
    Django's expectations for the database, so manual primary key
    setting is used on nearly every URY model.

    """
    return models.AutoField(
        primary_key=True,
        db_column=db_column)


def primary_key_from_meta(cls):
    """As 'primary_key', but infers the key name from model metadata.

    The resulting primary key name is the value of cls.db_table,
    with '_id' appended as per URY guidelines.

    """
    return primary_key(make_key_name(cls.db_table))


def make_key_name(db_table):
    """Converts a database table name into a URY-convention key name.

    """
    return '_'.join((db_table, 'id'))


def foreign_key(source_meta,
                dest,
                db_column,
                verbose_name=None):
    """Shortcut for creating a foreign key, given the source model's
    metadata class, the target model's class name and, optionally, the
    source database column and target model verbose name.

    """

    # Auto-infer a verbose name if none given.
    if verbose_name is None:
        verbose_name = dest.lower()

    format_tuple = (verbose_name, source_meta.verbose_name)
    return models.ForeignKey(
        dest,
        db_column=db_column,
        help_text='The %s this %s concerns.' % format_tuple)

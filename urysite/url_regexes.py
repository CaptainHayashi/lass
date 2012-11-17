"""
Common regular expression stubs for URLconfs.

These are collected in a common module to ensure consistency across
the LASS platform.

"""


# Helper functions #

def relative(partials):
    """
    Given a sequence of partial regexes, constructs a full regex that
    treats the partial regexes as stages in a directory hierarchy
    relative to the current root.

    """
    return r'^{0}/$'.format('/'.join(partials))


def relatives(partial_sequences):
    """
    A wrapper around `relative` that processes a sequence of partial
    regex sequences.

    """
    return (relative(x) for x in partial_sequences)


# Dates #

## Partial regexes
# NB: The year regex is limited to years 1-9999.
# This is intentional and mirrors the MAX_YEAR Python used at time of
# writing (thus preventing year overflows).
YEAR_PARTIAL = r'(?P<year>[1-9]\d?\d?\d?)'
WEEK_PARTIAL = r'[wW](eek)?(?P<week>([0-4]?\d|5[0-3]))'
WEEKDAY_PARTIAL = r'[dD]?(ay)?(?P<weekday>[1-7])'
MONTH_PARTIAL = r'(?P<month>(0?\d|1[12]))'
DAY_PARTIAL = r'(?P<day>([0-2]?\d|3[01]))'

## Full relative regexes
WEEK_REGEX, WEEKDAY_REGEX, DAY_REGEX = (
    relative(x) for x in (
        (YEAR_PARTIAL, WEEK_PARTIAL),
        (YEAR_PARTIAL, WEEK_PARTIAL, WEEKDAY_PARTIAL),
        (YEAR_PARTIAL, MONTH_PARTIAL, DAY_PARTIAL),
    )
)

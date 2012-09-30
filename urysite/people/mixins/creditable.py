"""The CreditableMixin, which is used to attach credits to a model.

"""


class CreditableMixin(object):
    """Mixin granting the ability to access credits."""

    ## MANDATORY OVERRIDES ##

    def credits_set(self):
        """Provides the set of this credit's metadata.

        Must be overridden in descended classes.

        """
        raise NotImplementedError('credits_set not implemented')

    ## PUBLIC METHODS ##

    # NB: Point credits_set to another item's credits_set if
    # credits for your item are stored in another item; you don't
    # need to override credits.
    def credits(self,
                from_date=None,
                to_date=None,
                exclude_unapproved=True):
        """Retrieves a set of credits for this object between the
        given dates inclusive.

        If 'from_date' and 'to_date' are not given, the default is
        item dependent but should be the time-span of the item itself
        where applicable and an infinite range otherwise.

        """
        from_date, to_date = self.ensure_range(from_date, to_date)

        credits = (self.credits_set().exclude(approver__isnull=True)
                   if exclude_unapproved
                   else self.credits_set().all())

        # Why excludes?  Because effective_to might be NULL
        # and we don't want to throw away results where it is
        # as this entails indefinite effectiveness.
        if from_date:
            credits.exclude(effective_from__gt=from_date)
        if to_date:
            credits.exclude(effective_to__lt=to_date)
        return credits

    ## ADDITIONAL METHODS ##

    def by_line(self, *args, **kwargs):
        """Returns a by-line - a human-readable summary of the most
        significant credits for this item.

        Arguments to this function are passed unchanged to credits()
        when retrieving the credits, so see the documentation for
        that function.

        The by-line does not include a 'with' or 'by' prefix.
        If nobody significant worked on the item, the empty string is
        returned.

        """
        credits = list(self.credits(*args, **kwargs))
        length = len(credits)
        if length == 0:
            by_line = ''
        elif length == 1:
            by_line = credits[0].person.full_name()
        else:
            by_line = u' and '.join((
                u', '.join(
                    cred.person.full_name() for cred in credits[:-1]),
                credits[-1].person.full_name()))
        return by_line

    ## INTERNAL SUPPORT METHODS ##

    def ensure_range(self, from_date, to_date):
        """Given a date range that may include None values, attempts
        to fill in the potential Nones with the item's own range
        values if such values exist.

        """
        try:
            # Implementors of DateRangeMixin'll have this method
            item_from, item_to = self.date_range()
        except AttributeError:
            # Nope, we'll just use an infinite range instead
            item_from, item_to = None, None

        return (item_from if from_date is None else from_date,
                item_to if to_date is None else to_date)

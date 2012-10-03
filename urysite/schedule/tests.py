"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from schedule.models import Timeslot
from schedule.utils import filler
from django.utils import timezone
from datetime import timedelta


class FillEmptyRange(TestCase):
    """Tests whether the filling algorithm correctly handles an empty
    timeslot list."""
    def setUp(self):
        self.timeslots = []
        self.duration = timedelta(hours=2)
        self.past_time = timezone.now()
        self.future_time = timezone.now() + self.duration

    def test_normal_fill(self):
        """Tests whether an attempt to fill an empty list returns a
        single filler slot spanning the entire requested range.

        """
        filled = filler.fill(
            self.timeslots,
            self.past_time,
            self.future_time
        )
        self.AssertTrue(len(filled) == 1)
        
        filler_slot = filled[0]
        self.assertTrue(isinstance(filler_slot, Timeslot))
        self.assertEqual(filler_slot.start_time, self.past_time)
        self.assertEqual(filler_slot.duration, self.duration)

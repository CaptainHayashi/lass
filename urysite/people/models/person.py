"""Models pertaining to people and various subtypes of people."""

from django.db import models
from urysite import model_extensions as exts


class Person(models.Model):
    """A person tracked by the URY people database.

    A person, despite the name of the database table, is not
    necessarily a URY member.  The people database also tracks:

    * People who have left URY
    * Honorary members
    * People who have joined URY but not yet paid membership dues
    * People who have signed up to join URY but have not yet done so

    """

    class Meta:
        db_table = 'member'
        managed = False
        app_label = 'people'

    def full_name(self):
        """Retrieves the full name of this person.

        The full name is in the format FIRSTNAME LASTNAME, as per
        Western customs.

        """
        return u'%s %s' % (self.first_name, self.last_name)

    def full_name_reverse(self):
        """Retrieves the reverse-order full name of this person.

        The result will be in the format LASTNAME, FIRSTNAME (with
        the comma).

        """
        return u'%s, %s' % (self.last_name, self.first_name)

    def __unicode__(self):
        """Retrieves this person's Unicode representation.

        Currently, this is just their full name.

        """
        return self.full_name()

    id = exts.primary_key('memberid')

    first_name = models.CharField(
        max_length=255,
        db_column='fname')

    last_name = models.CharField(
        max_length=255,
        db_column='sname')

    gender = models.CharField(
        max_length=1,
        db_column='sex')

    college = models.IntegerField()

    phone = models.CharField(max_length=255)

    email = models.EmailField(max_length=255)

    receive_email = models.BooleanField(default=True)

    local_name = models.CharField(max_length=100)

    local_alias = models.CharField(max_length=32)

    password = models.CharField(max_length=255)

    account_locked = models.BooleanField(default=False)

    last_login = models.DateTimeField()

    end_of_course = models.DateTimeField(db_column='endofcourse')

    eduroam = models.CharField(max_length=255)  # unlimited in DB atm

    use_smtp_password = models.BooleanField(
        default=False,
        db_column='usesmtppassword')

    date_joined = models.DateTimeField(
        auto_now_add=True,
        db_column='joined')



####################
## Person proxies ##
####################

# These two models are used to make the case where multiple people
# are associated with a model (in different ways- for example creator
# of a data item, approver of that item, etc) less ambiguous.

class Creator(Person):
    """A creator of show data."""
    class Meta:
        proxy = True
        app_label = 'people'


class Approver(Person):
    """A person who has approved a schedule change."""
    class Meta:
        proxy = True
        app_label = 'people'

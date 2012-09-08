from django.db import models


## LeRouge #

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

    id = models.AutoField(
        primary_key=True,
        db_column='memberid')

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


class RoleVisibility(models.Model):
    class Meta:
        db_table = 'visibilities'
        managed = False

    def __unicode__(self):
        return self.name

    id = models.AutoField(
        primary_key=True,
        db_column='visibilitylevel')

    name = models.CharField(max_length=100)

    description = models.TextField()


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


class Approver(Person):
    """A person who has approved a schedule change."""
    class Meta:
        proxy = True


###########
## Roles ##
###########

class Role(models.Model):
    class Meta:
        db_table = 'roles'  # in schema 'people'
        managed = False

    def __unicode__(self):
        return self.alias

    id = models.AutoField(
        primary_key=True,
        db_column='roleid')

    alias = models.CharField(max_length=100)

    visibility_level = models.ForeignKey(
        RoleVisibility,
        db_column='visibilitylevel')

    is_group_root = models.BooleanField(
        db_column='isgrouproot')

    is_active = models.BooleanField(
        db_column='isactive')

    ordering = models.IntegerField()

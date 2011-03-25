from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models import permalink


class Price(models.Model):
    amount = models.DecimalField(decimal_places=2,
                                 max_digits=4)

    def __unicode__(self):
        return "UKP%.2f" % self.amount


class Venue(models.Model):
    name = models.CharField(max_length=40)
    lat = models.FloatField(blank=True,
                            null=True)
    lon = models.FloatField(blank=True,
                            null=True)


class Event(models.Model):
    name = models.CharField(max_length=40)
    gender = models.CharField(max_length=1,
                              choices=(('m', 'men'),
                                       ('f', 'women'),
                                       ('b', 'mixed')))

    def __unicode__(self):
        return "%s's %s" % (self.gender,
                            self.name)


class Discipline(models.Model):
    name = models.CharField(max_length=40)


class Session(models.Model):
    discipline = models.ForeignKey(Discipline)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    medal_session = models.BooleanField()
    limit = models.IntegerField()
    prices = models.ManyToManyField(Price)
    venue = models.ForeignKey(Venue)
    events = models.ManyToManyField(Event)

    def __unicode__(self):
        return "%s on %s; %s" % (self.discipline.name,
                                 self.starts.strftime("%d/%m"),
                                 self.events.all())

    @permalink
    def get_absolute_url(self):
        return ("session", (self.id,))


class CustomUser(User):
    objects = UserManager()

    @property
    def display_name(self):
        if self.first_name:
            name = self.first_name
        else:
            name = self.email
        return name

    def __unicode__(self):
        return self.email

    @permalink
    def get_absolute_url(self):
        return ("user", (self.id,))

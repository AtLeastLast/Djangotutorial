from django.db import models
from django.contrib.auth.models import User


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField('Address', max_length=120)
    zip_code = models.CharField('Zip Code', max_length=10)
    phone = models.CharField('Contact Phone', max_length=120, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)

    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name = models.CharField('First Name', max_length=120)
    last_name = models.CharField('Last Name', max_length=120)
    email = models.EmailField('Email Address')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    #venue = models.CharField('Venue', max_length=60)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField('Description', max_length=500, blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True, null=True)

    def __str__(self):
        return self.name
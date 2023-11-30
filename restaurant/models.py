from django.db import models

class Menu(models.Model):
    """ class for the Menu"""
    menuItem = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=500, null=False)
    price = models.IntegerField(null=False)

class Bookings(models.Model):
    """ class for bookings """
    name = models.CharField(max_length=200)
    slots = models.IntegerField(default=2)
    date = models.DateField(null=False)
from django.db import models
from django.contrib.auth.models import User

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

class Cart(models.Model):
    """ cart """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    totalprice = models.DecimalField(decimal_places=2, max_digits=65)

class Orders(models.Model):
    """ Order """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crew_member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crew')
    status = models.BooleanField(default=False)
    totalPrice = models.DecimalField(decimal_places=2, max_digits=65)

class OrderItem(models.Model):
    """ orderItem """
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE) 
    quentity = models.IntegerField()
    totalPrice= models.DecimalField(max_digits=65 ,decimal_places=2)
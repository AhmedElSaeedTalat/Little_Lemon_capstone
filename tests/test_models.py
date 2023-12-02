from django.test import TestCase
from restaurant.models import Menu, Bookings
from datetime import date
""" module to for test cases """


class MenuTest(TestCase):
    """ test Menu """
    def test_menuCreate(self):
        """ test create menu item """
        menu = Menu.objects.create(menuItem= 'cake', price=50)
        self.assertEqual(str(menu), 'cake: 50$')

class BookingTest(TestCase):
    """ test Booking """
    def test_bookingCreate(self):
        """ test create a booking """
        booking = Bookings.objects.create(name='James', slots=3, date=date(2023, 12, 5))
        self.assertEqual(str(booking), 'booking name: James')
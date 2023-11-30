from django.shortcuts import render
from django.views import View
from restaurant.forms import BookingForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .models import Bookings
from .serializers import BookingsSerializers
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.
def home(request):
    """ view function for home page """
    return render(request, 'index.html')

def menu(request):
    """ return menu page """
    return render(request, 'menu.html')

class BookView(View):
    """ class for booking tempates """
    def get(self, request):
        """ display booking page """
        form = BookingForm()
        context = {'form': form}
        return render(request, 'book.html', context)
    def post(self, request):
        """ post booking data"""
        data = json.load(request)
        form = BookingForm(data)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
        else:
            return HttpResponse(status=400)
        
def bookingView(request):
    """ display all bookings """
    bookings = Bookings.objects.all()
    context = {'bookings': bookings}
    return render(request, 'booking.html', context)

""" API Views """
class ReservationsApi(viewsets.ViewSet):
    """ display api """
    def list(self, request):
        """ list all bookings """
        query_set = Bookings.objects.all()
        serializer = BookingsSerializers(query_set, many=True)
        return Response(serializer.data)

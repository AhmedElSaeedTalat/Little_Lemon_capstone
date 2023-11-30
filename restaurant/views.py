from django.shortcuts import render
from django.views import View
from restaurant.forms import BookingForm

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
        form = BookingForm(request.POSt)
        if form.is_valid():
            form.save()
        return 'success'
        
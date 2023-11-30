from django.shortcuts import render
from django.views import View

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
        return render(request, 'book.html')
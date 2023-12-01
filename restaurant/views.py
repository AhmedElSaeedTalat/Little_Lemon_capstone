from django.shortcuts import render
from django.views import View
from restaurant.forms import BookingForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from .models import Bookings, Menu, Cart, Orders, OrderItem
from .serializers import BookingsSerializers, MenuSerializer,\
CartSerializers, OrderSerializers, OrderItemSerializers
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404


# views here.
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

    @action(detail=False, methods=['POST'])
    def post(self, request):
        """ function to create booking through API """
        serializer = BookingsSerializers(data=request.data)
        if serializer.is_valid():
            booking = Bookings.objects.create(
                name = serializer.validated_data['name'],
                date = serializer.validated_data['date'],
                slots = serializer.validated_data['slots']
            )
            booking.save()
            return Response(serializer.data)

class MenuApiView(viewsets.ViewSet):
    """ class to view menu items and post to it"""
    def list(self, request):
        """ list Menu items """
        query_set = Menu.objects.all()
        serializer = MenuSerializer(query_set, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def post(self, request):
        """ function to add menu items """
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            menu = Menu(
                menuItem = serializer.validated_data['menuItem'],
                description = serializer.validated_data['description'],
                price = serializer.validated_data['price']
            )
            menu.save()
            return Response(serializer.data)

@permission_classes([IsAuthenticated])
class CartApiView(viewsets.ViewSet):
    """ list cart and post to cart """
    def list(self, request):
        query_set = Cart.objects.filter(user=request.user).all()
        serializer = CartSerializers(query_set, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'])
    def post(self, request):
        """ post to cart """
        user_id = request.user.id
        data = request.data
        item_id = data['item']
        quantity = data['quantity']
        item = get_object_or_404(Menu, id=item_id)
        price = item.price
        totalprice = price * quantity
        data['totalprice'] = totalprice
        data['user'] = user_id
        data['item'] = item_id
        serializer = CartSerializers(data=data)
        if serializer.is_valid():
            cart = Cart.objects.create(
                item = serializer.validated_data['item'],
                user = serializer.validated_data['user'],
                quantity = serializer.validated_data['quantity'],
                totalprice = serializer.validated_data['totalprice']
            )
            cart.save()
            return Response(serializer.data)
        else:
            errors = serializer.errors
            print(errors)
            return Response('not valid')

@permission_classes([IsAuthenticated])
class OrdersApiView(viewsets.ViewSet):
    """ 
    class to place orders
    orders are created and orderItems related also
    """
    def list(self, request):
        """ list all orders """
        if request.user.groups.filter(name='Maneger').exists():
            orders = Orders.objects.all()
        else:
            user_id = request.user.id
            orders = Orders.objects.filter(user=get_object_or_404(User, id=user_id)).all()
        serializer = OrderSerializers(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'])
    def post(self, request):
        """ create orders """
        user_id = request.user.id
        user = get_object_or_404(User, id=user_id)
        cart = Cart.objects.filter(user=user).all()
        """ create order """
        sum = 0
        for item in cart:
            sum += item.totalprice
        order = Orders.objects.create(
            user = user,
            totalPrice = sum
        )
        order.save()
        """ create order items  and relate them to order created """
        for element in cart:
            order_item = OrderItem.objects.create(
                order = order,
                item = element.item,
                quentity = element.quantity,
                totalPrice = element.totalprice
            )
            order_item.save()
        
        """ delete cart objects """
        cart = Cart.objects.filter(user=user_id).delete()
        """ display order created """
        serializer = OrderSerializers(order)
        return Response(serializer.data)
    
@permission_classes([IsAuthenticated])
class OrderItemApiView(viewsets.ViewSet):
    """ list order items """
    def list(self, request):
        user = get_object_or_404(User, id=request.user.id)
        orders = user.order.all()
        items = []
        for order in orders:
            items.extend(order.orderItem.all())
        serializer = OrderItemSerializers(items, many=True)
        return Response(serializer.data)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('bookings', views.ReservationsApi, basename='bookings')
router.register('menu', views.MenuApiView, basename='menu')
router.register('cart', views.CartApiView, basename='cart')
urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
from rest_framework import serializers
from .models import Bookings

class BookingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = '__all__'
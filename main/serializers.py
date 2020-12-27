from .models import *

from rest_framework import serializers

from django.db.models import Q


class WorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        """
        Check that the booking begin is before the booking end.
        """
        if data['booking_begin'] >= data['booking_end']:
            raise serializers.ValidationError("Booking begin-timestamp have to be before end-timestamp")

        # Check if time interval is already taken
        if Booking.objects.filter(
                Q(workplace_id=data['workplace']), Q(removed_at__isnull=True),
                (Q(booking_begin__lte=data['booking_begin']) & Q(booking_end__gte=data['booking_end'])) |
                (Q(booking_begin__gte=data['booking_begin']) & Q(booking_begin__lte=data['booking_end'])) |
                (Q(booking_end__gte=data['booking_begin']) & Q(booking_end__lte=data['booking_end']))):
            raise serializers.ValidationError("Booking timestamp is already taken.")
        return data

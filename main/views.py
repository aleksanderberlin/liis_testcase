from .serializers import *

from django.http import Http404
from django.utils import timezone

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class WorkplaceList(APIView):
    """
    List all workplaces and manage them.
    """

    def get_object(self, pk):
        try:
            return Workplace.objects.get(pk=pk)
        except Workplace.DoesNotExist:
            raise Http404

    def get(self, request):
        if 'datetime_from' in request.query_params and 'datetime_to' in request.query_params:
            try:
                datetime_from = datetime.fromisoformat(request.query_params['datetime_from'])
                datetime_to = datetime.fromisoformat(request.query_params['datetime_to'])
            except ValueError:
                return Response('Incorrect datetime format', status=status.HTTP_400_BAD_REQUEST)

            taken_timeslots = Booking.objects.filter(
                Q(removed_at__isnull=True),
                (Q(booking_begin__lte=datetime_from) & Q(booking_end__gte=datetime_to)) |
                (Q(booking_begin__gte=datetime_from) & Q(booking_begin__lte=datetime_to)) |
                (Q(booking_end__gte=datetime_from) & Q(booking_end__lte=datetime_to)))

            workplaces = Workplace.objects.exclude(id__in=taken_timeslots.values('workplace_id'))
        else:
            workplaces = Workplace.objects.all()
        serializer = WorkplaceSerializer(workplaces, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkplaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkplaceDetail(APIView):
    """
    Retrieve, update or delete a workplace object.
    """

    def get_object(self, pk):
        try:
            return Workplace.objects.get(pk=pk)
        except Workplace.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        workplace = self.get_object(pk)
        workplace = WorkplaceSerializer(workplace)
        return Response(workplace.data)

    def put(self, request, pk, format=None):
        workplace = self.get_object(pk)
        serializer = WorkplaceSerializer(workplace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        workplace = self.get_object(pk)
        workplace.removed_at = timezone.now()
        workplace.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingList(APIView):
    """
    List all workplaces and manage them.
    """

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    def get(self, request):
        if 'workplace_id' in request.query_params:
            bookings = Booking.objects.filter(workplace_id=request.query_params['workplace_id'])
        else:
            bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingDetail(APIView):
    """
    Retrieve, update or delete a workplace object.
    """

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        booking = self.get_object(pk)
        booking = BookingSerializer(booking)
        return Response(booking.data)

    def put(self, request, pk, format=None):
        booking = self.get_object(pk)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        booking = self.get_object(pk)
        booking.removed_at = timezone.now()
        booking.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

import requests

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from rest_framework.permissions import AllowAny

from .models import Room, Booking, CheckIn
from .serializer import (
    RoomSerializer,
    BookingSerializer,
    CheckinSerializer
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)

from .utils import *


class RoomView(ListAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.order_by('-id')

    def get(self, request):
        rooms, search_query = searchRooms(request)
        paginated_data = paginateRooms(request, rooms)

        serializer = RoomSerializer(paginated_data["rooms"], many=True)
        return Response({
            "rooms": serializer.data,
            "current_page": request.GET.get('page', 1),
            "search_query": search_query,
            "total_rooms": len(rooms),
        })



class RoomDetailView(RetrieveAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    lookup_field = 'room_slug'


class BookingCreateApiView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def create(self, request, *args, **kwargs):
        response = {}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response['data'] = serializer.data
        response['response'] = "Room is successfully booked"
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        room = get_object_or_404(Room, pk=request.data['room'])
        if room.is_booked:
            return Response({"response": "Room is already booked"}, status=status.HTTP_200_OK)
        room.is_booked = True
        room.save()
        checked_in_room = CheckIn.objects.create(
            customer=request.user,
            room=room,
            phone_number=request.data['phone_number'],
            email=request.data['email']
        )
        checked_in_room.save()
        return self.create(request, *args, **kwargs)


class CheckoutView(APIView):

    @swagger_auto_schema(
        request_body=CheckinSerializer,
        responses={201: CheckinSerializer},
    )
    def post(self, request):
        room = get_object_or_404(Room, pk=request.data['pk'])
        checked_in_room = CheckIn.objects.get(room__pk=request.data['pk'])
        room.is_booked = False
        room.save()
        checked_in_room.delete()
        return Response({"Checkout Successful"}, status=status.HTTP_200_OK)


class CheckedInView(ListAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = CheckinSerializer
    queryset = CheckIn.objects.order_by('-id')


class CurrencyLayer(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        url = f"http://v6.exchangerate-api.com/v6/{settings.CURRENCYLAYER_API_KEY}/latest/USD"
        response = requests.get(url, verify=True)
        if response.status_code != 200:
            return JsonResponse({"error": "Currency data not available"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json()
        return JsonResponse(data)


class Weather(APIView):
    permission_classes = [AllowAny]
    def get(self, request, city):
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHERMAP_API_KEY}'
        response = requests.get(url, verify=True)
        if response.status_code != 200:
            return JsonResponse({"error": "Weather data not available"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json()
        return JsonResponse(data)
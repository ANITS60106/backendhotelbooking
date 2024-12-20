from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    RoomView, RoomDetailView, CurrencyLayer,
    BookingCreateApiView, CheckoutView, CheckedInView
)

app_name = 'hotel_app'

urlpatterns = [
    path('hotel/get_room_list/', RoomView.as_view(), name="room_list"),
    path('hotel/get_a_room_detail/<str:room_slug>/', RoomDetailView.as_view(), name="single_room"),
    path('hotel/book/', BookingCreateApiView.as_view(), name='book_room'),
    path('hotel/checkout/', CheckoutView.as_view(), name="checkout"),
    path('hotel/get_current_checked_in_rooms/', CheckedInView.as_view(), name="checked_in_rooms"),
    path('hotel/currency-layer/', CurrencyLayer.as_view(), name='currency-layer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

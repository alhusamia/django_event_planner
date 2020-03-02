"""event_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from API import views as secondview


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('event/list/', views.eventlist, name='event-list'),
    path('event/my_list/', views.my_list, name='my-list'),
    path('event/my_booking/', views.my_booking, name='my-booking'),
    path('event/user_update/', views.user_update, name='user-update'),

    path('event/<int:event_id>/detail/reserving/', views.reserve_event, name='reserve-event'),

    path('event/create/', views.event_create, name='event-create'),
    path('event/<int:event_id>/detail/', views.event_detail, name='event-detail'),
    path('event/<int:event_id>/detail/follow', views.follow, name='follow'),
    path('event/<int:event_id>/update/', views.event_update, name='event-update'),
    path('event/<int:event_id>/delete/',views.Event_delete ,name='event-delete'),



    path('api/list', secondview.EventListView.as_view(), name="api-list"),
    path('api/booking_list', secondview.BookingListView.as_view(), name="api-booking-list"),
    path('api/Specificbooking/<str:user_username>', secondview.SpecificListView.as_view(), name="api-user-list"),
    path('api/booking/<int:event_id>/create/', secondview.CreateBookingView.as_view(), name="create-booking"),
    path('api/bookingdetail/<int:event_id>/',secondview.BookingDetailView.as_view(), name='booking-detail'),
    path('register/', secondview.Register.as_view(), name="register"),
    path('api/<int:event_id>/create', secondview.CreateEventView.as_view(), name="create-event"),
    path('api/<int:event_id>/update/', secondview.UpdateEventView.as_view(), name="update-event"),
    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),
]


if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

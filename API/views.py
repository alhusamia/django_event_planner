from django.shortcuts import render
from rest_framework.generics import ListAPIView , CreateAPIView,RetrieveUpdateAPIView ,RetrieveAPIView,DestroyAPIView
from .serializers import  ListSerializer, BookingListSerializer, UserSerializer, RegisterSerializer, EventCreateSerializer, UpdateEventSerializer, BookingCreateSerializer, BookingDetailSerializer, FollowingListSerializer, FollowingCreateSerializer
from events.models import Event,Booking,Profile,Follow
from .permissions import IsAny
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from datetime import datetime
class EventListView(ListAPIView):
    queryset = Event.objects.filter(date__gt=datetime.today())
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated, IsAny]

class BookingListView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated,  IsAny]

class SpecificListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAny]
    def get_queryset(self):
        user = self.kwargs['user_username']
        return Event.objects.filter(user__username = user )

class Register(CreateAPIView):
    serializer_class = RegisterSerializer
    # permission_classes = [IsAny]

class CreateEventView(CreateAPIView):
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpdateEventView(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventCreateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
##########################################################################################################
class CreateBookingView(CreateAPIView):
    serializer_class = BookingCreateSerializer
    def perform_create(self, serializer):
        serializer.save(visitor=self.request.user, event_id=self.kwargs['event_id'])

class BookingDetailView(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    # permission_classes = [IsAny]

####################################views-API#######################################################################
class FollowingListView(ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowingListSerializer
    permission_classes = [IsAuthenticated , IsAny]

class CreateFollowingView(CreateAPIView):
    serializer_class = FollowingCreateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
        
class DeleteFollowingView(DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowingListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'follower_id'

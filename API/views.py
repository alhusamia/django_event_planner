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
class EventListView(ListAPIView):#list of upcoming events
    queryset = Event.objects.filter(date__gt=datetime.today())
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated, IsAny]

class BookingListView(ListAPIView):#list of events i have booked for ,as a logged in user
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated,  IsAny]

class SpecificListView(ListAPIView):#list of events for a specific organizer
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAny]
    def get_queryset(self):
        user = self.kwargs['user_username']
        return Event.objects.filter(user__username = user )

class Register(CreateAPIView):#signup
    serializer_class = RegisterSerializer
    #permission_classes = [IsAny, IsAuthenticated]

class CreateEventView(CreateAPIView):#create an event
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpdateEventView(RetrieveUpdateAPIView):#update an event
	queryset = Event.objects.all()
	serializer_class = EventCreateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
##########################################################################################################
class CreateBookingView(CreateAPIView):#create an event
    serializer_class = BookingCreateSerializer
    def perform_create(self, serializer):
        serializer.save(visitor=self.request.user, event_id=self.kwargs['event_id'])

class BookingDetailView(RetrieveAPIView):#as a user I can retrieve a list of people who have booked for an event
    queryset = Booking.objects.all()
    serializer_class = BookingDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    # permission_classes = [IsAny]

####################################views-API#######################################################################
class FollowingListView(ListAPIView):#list of organizers  I am following, as a logged in user
    queryset = Follow.objects.all()
    serializer_class = FollowingListSerializer
    permission_classes = [IsAuthenticated , IsAny]

class CreateFollowingView(CreateAPIView):#as a user I can follow an organizer
    serializer_class = FollowingCreateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

class DeleteFollowingView(DestroyAPIView):#as a user I can unfollow an organizer
    queryset = Follow.objects.all()
    serializer_class = FollowingListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'follower_id'

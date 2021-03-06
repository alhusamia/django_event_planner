from rest_framework import serializers
from events.models import Event,Booking,Follow
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date','time', 'location','seats','user']


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date','time', 'location','seats','user']
class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['visitor','event']
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data
class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['user']
class UpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date','time', 'location','seats','user']

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['reserved_num']


class BookingDetailSerializer(serializers.ModelSerializer):
     class Meta:
        model = Booking
        fields = ['visitor','reserved_num',]

###########################################################################

class AddedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
class FollowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['slug']
class FollowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        exclude = [ 'follower']

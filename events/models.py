from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=120)
    datetime = models.DateTimeField()
    seats = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def booked_seats(self):
        return sum(self.bookings.all().values_list('reserved_num', flat=True))

    def get_seat_left(self):
        return (self.seats- self.booked_seats())

class Booking(models.Model):
    visitor=  models.ForeignKey(User, on_delete=models.CASCADE)
    reserved_num = models.PositiveIntegerField()
    event= models.ForeignKey(Event, on_delete=models.CASCADE,related_name='bookings')

from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=120)
    datetime = models.DateTimeField()
    seats = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def counter(self):
        bookings = self.booking_set.all()
        num = 0
        for n in bookings:            
            num += n.reserved_num
        return num



class Booking(models.Model):
    visitor=  models.ForeignKey(User, on_delete=models.CASCADE)
    reserved_num = models.PositiveIntegerField()
    event= models.ForeignKey(Event, on_delete=models.CASCADE)

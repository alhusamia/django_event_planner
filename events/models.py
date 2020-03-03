from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Event(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=120)
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    seats = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="events")
    def booked_seats(self):
        return sum(self.bookings.all().values_list('reserved_num', flat=True))

    def get_seat_left(self):
        return (self.seats- self.booked_seats())

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    # follower = models.ManyToManyField('Profile', related_name="followed_by",symmetrical=False,default=None)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Booking(models.Model):
    visitor=  models.ForeignKey(User, on_delete=models.CASCADE)
    reserved_num = models.PositiveIntegerField()
    event= models.ForeignKey(Event, on_delete=models.CASCADE,related_name='bookings')
# class Follow(models.Model):
#     follower = models.

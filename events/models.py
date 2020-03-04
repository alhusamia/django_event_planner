from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save , pre_save
from django.template.defaultfilters import slugify
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

class Follow(models.Model):
    follower = models.ForeignKey(User , related_name="follower",on_delete=models.CASCADE)
    following =models.ForeignKey(User , related_name="following",on_delete=models.CASCADE)
##########################################################################################################################
    slug = models.SlugField(blank=True)
def create_slug(instance, new_slug=None):
    slug = slugify(instance.following)
    if new_slug is not None:
        slug = new_slug
    qs = Follow.objects.filter(slug=slug)
    if qs.exists():
        try:
            int(slug[-1])
            if "-" in slug:
                slug_list = slug.split("-")
                new_slug = "%s%s" % (slug[:-len(slug_list[-1])], int(slug_list[-1]) + 1)
            else:
                new_slug = "%s-1" % (slug)
        except:
            new_slug = "%s-1" % (slug)
        return create_slug(instance, new_slug=new_slug)
    return slug
@receiver(pre_save, sender=Follow)
def generate_slug(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)

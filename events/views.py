from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views import View
from datetime import datetime
from .forms import UserSignup,UserLogin,UserForm,EventForm,ReserveForm,ProfileForm
from django.contrib import messages
from .models import Event,Profile, Booking,Follow
from django.db.models import Q
from django.utils import timezone
def home(request):
    return render(request, 'home.html')

#======= Dashboard ========#
def dashboard(request):
    event = Event.objects.all()
    context = {
        'event':event
    }
    return render(request,'dashboard.html',context)

#======= My list ========#
def my_list(request):
    event = Event.objects.all()
    if request.user.is_anonymous:
        return redirect('login')

    events = Event.objects.filter(user = request.user)
    if request.user:
        events.user = request.user
        context = {
            'events': events,
            }
    return render(request,'mylist.html',context)
#======= My booking  ========#
def my_booking(request):
    bookings = Booking.objects.all()
    if request.user.is_anonymous:
        return redirect('login')

    context={
    'bookings':bookings
    }
    return render(request,'past_booking.html',context)
#======= Event list ========#
def eventlist(request):
    events = Event.objects.filter(date__gt =datetime.today())
    if request.user.is_anonymous:
        return redirect('login')

    query = request.GET.get("q")
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(user__username__icontains=query)
            ).distinct()


    context = {
        'events':events,
    }
    return render(request,'eventlist.html',context)

#======= Create Event ========#
def event_create(request):
    form = EventForm()
    if request.user.is_anonymous:
        return redirect('login')

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES or None)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, "Successfully Created!")
            return redirect('event-list')
        print (form.errors)
    context = {
    "form": form,
    }
    return render(request, 'create.html', context)


#======= Event Detail ========#
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    user = event.user
    if request.user.is_anonymous:
        return redirect('login')

    bookings = Booking.objects.filter(event=event)
    # follow = Follow.objects.filter(following=event)
    context = {
        "event": event,
        'bookings':bookings,
        'user':user
    }
    return render(request, 'event_detail.html', context)

#======= Event Update ========#
def event_update(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user.is_anonymous:
        return redirect('login')

    form = EventForm(instance=event)
    if not request.user == event.user:
        return redirect('event-list')
    if request.method == "POST":
        form = EventForm(request.POST,request.FILES, instance=event )
        if form.is_valid():
            form.save()
            messages.success(request, 'event details updated.')
            return redirect('event-list')

    context = {
        "event": event,
        "form":form,

    }
    return render(request, 'updatedetails.html', context)

#======= His Event  ========#
def his_event(request,user_id):
     if request.user.is_anonymous:
         return redirect('login')

     events = Event.objects.filter(user = user_id)
     events.user = request.user
     context = {
        'events': events,
             }
     return render(request,'profile_user.html',context)
#======= Event Delete ========#
def Event_delete(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    if request.user.is_anonymous:
        return redirect('login')
    if not request.user == event_obj.user:
        return redirect('event-list')

    event_obj.delete()
    return redirect('event-list')

# ================reserve an event==================
def reserve_event(request,event_id):
    if request.user.is_anonymous:
        return redirect('login')
    event =Event.objects.get(id=event_id)
    form = ReserveForm()

    if request.method == "POST":
        form = ReserveForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.visitor = request.user
            booking.event = event
            seats = event.get_seat_left()
            if booking.reserved_num <= seats:
                booking.save()
                send_mail(
                'Detail Booking:',
                f"The number of Ticket {{booking.reserved_num}}  The Booker was {{booking.visitor}}",
                'tt0170712@gmail.com',
                [booking.visitor.email],
                fail_silently=False,
                )
                messages.success(request, "Successfully Reserved")
                return redirect('event-detail', event_id)
            else:
                messages.warning(request,'Not Enough seats!')


    context = {
        "form":form,
        'event':event
    }
    return render(request, 'index.html', context)
#=============Profile User ========#
def profile_user(request,user_id):
    profile = Profile.objects.get(user_id = user_id)
    events = Event.objects.filter(user_id=user_id)
    context={
    'profile':profile,
    'events':events
    }
    return render(request,'profile_user.html',context)
#======= update User ========#
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile_form.save()
            login(request, user)
            messages.success(request,('Your profile was successfully updated!'))
            return redirect('event-list')
        else:
            messages.error(request,('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    context={
    'user_form': user_form,
    'profile_form': profile_form,
    }
    return render(request, 'profile.html', context)
#========== follow =============#
def follow(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user.is_anonymous :
        return redirect('login')
    if Follow.objects.filter(follower=request.user,following=user).count()>0:
        messages.warning(request, "You have already followed this user")
        return redirect('profile-user',user_id)
    follow= Follow(follower=request.user,following=user)
    follow.save()
    messages.success(request, ('His profile was successfully Followed!'))
    return redirect ('event-list')

#===========Unfollow============#
def unfollow(request,user_id):
    user = User.objects.get(id=user_id)
    if request.user.is_anonymous :
        return redirect('login')
    if  request.user.is_staff or request.user == user:
        unfollow = Follow.objects.filter(follower=request.user,following=user).delete()
        messages.warning(request, "You have already Unfollowed this user")
        return redirect('profile-user',user_id)


class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("event-list")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('event-list')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

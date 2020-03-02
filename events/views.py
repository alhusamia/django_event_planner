from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from datetime import datetime
from .forms import UserSignup,UserLogin,UserFrom,EventForm,ReserveForm
from django.contrib import messages
from .models import Event,Booking,Follow
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
        return redirect('signin')

    events = Event.objects.filter(user = request.user)
    if request.user:
        events.user = request.user
        context = {
            'events': events,
            }
    return render(request,'mylist.html',context)
#======= My booking  ========#
def my_booking(request):
    bookings = Booking.objects.filter(event__date__lt=datetime.today())
    if request.user.is_anonymous:
        return redirect('signin')

    context={
    'bookings':bookings
    }
    return render(request,'past_booking.html',context)
#======= Event list ========#
def eventlist(request):
    events = Event.objects.filter(date__gt =datetime.today())
    if request.user.is_anonymous:
        return redirect('signin')

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
        return redirect('signin')

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
    if request.user.is_anonymous:
        return redirect('signin')

    bookings = Booking.objects.filter(event=event)
    follow = Follow.objects.filter(following=event)
    context = {
        "event": event,
        'bookings':bookings,
        'follow':follow
    }
    return render(request, 'event_detail.html', context)

#======= Event Update ========#
def event_update(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user.is_anonymous:
        return redirect('signin')

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
#======= Event Delete ========#
def Event_delete(request, event_id):
    event_obj = Event.objects.get(id=event_id)
    if request.user.is_anonymous:
        return redirect('signin')

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
                messages.success(request, "Successfully Reserved")
                return redirect('event-detail', event_id)
            else:
                messages.warning(request,'Not Enough seats!')


    context = {
        "form":form,
        'event':event
    }
    return render(request, 'index.html', context)

#======= update User ========#
def user_update(request):

    if request.user.is_anonymous:
        return redirect('signin')

    form = UserForm(instance=request.user)
    if request.method == "POST":
        form = UserForm(request.POST,instance=request.user )
        if form.is_valid():
            form.save()
            messages.success(request, 'User details updated.')
            return redirect('event-list')

    context = {
        "event": event,
        "form":form,

    }
    return render(request, 'update_user.html', context)

#========== follow =============#
def follow(request,event_id):
    event = Event.objects.get(id=event_id)
    if request.user.is_anonymous:
        return redirect('user-login')
    follow = Follow(following=event,follower=request.user)
    follow.save()
    return redirect('event-detail',event_id)
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

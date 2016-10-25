from django.shortcuts import render, redirect, HttpResponse
from ..login_app.models import User
from .models import Trip
from django.core.urlresolvers import reverse
from django.contrib import messages

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'data': user,
            'users': Trip.objects.all().filter(group=user),
            'trips': Trip.objects.all().exclude(group=user)
        }
        return render(request, 'travel_app/index.html', context)
    else:
        return redirect(reverse('login:index'))

def add(request):
    return render(request, 'travel_app/add.html')

def process(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        result = Trip.objects.addTrip(request.POST, user)
        if result[0] == True:
            messages.success(request, result[1])
            return redirect(reverse('travel:index'))
        else:
            for error in result[1]:
                messages.error(request, error)
            return redirect(reverse('travel:add'))

def destination(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    context = {
        'trips': trip,
        'group': trip.group.all()
    }
    return render(request,'travel_app/destination.html', context)

def join(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    result = Trip.objects.joinTrip(trip_id, user)
    messages.success(request, result[1])
    return redirect(reverse('travel:index'))

# def delete(request, trip_id):
#     Trip.objects.get(id=trip_id).delete()
#     messages.success(request, "Successfully deleted")
#     return redirect(reverse('travel:index'))

# def cancel(request, trip_id):
#     u = User.objects.get(id=request.session['user'])
#     trip = Travel.objects.get(id=trip_id)
#     trip.users.remove(u)
#     messages.success(request, "Trip cancelled.")
#     return redirect(reverse('travel:index'))


def logout(request):
    request.session.clear()
    return redirect(reverse('login:index'))

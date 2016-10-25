from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect(reverse('travel:index'))
    else:
        return render(request, 'login_app/index.html')

def register(request):
    result = User.objects.register(request.POST)
    if result[0] == True:
        request.session['user_id'] = result[1].id
        messages.success(request, "Hello! You have successfully registered! Now please log in.")
        return redirect(reverse('login:index'))
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect(reverse('login:index'))

def login(request):
    result = User.objects.login(request.POST)
    if result[0] == True:
        request.session['user_id'] = result[1].id
        return redirect(reverse('travel:index'))
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect(reverse('login:index'))

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "You have been successfully logged out")
        return redirect(reverse('login:index'))

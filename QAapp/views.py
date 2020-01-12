from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth.models import User,auth
from django.middleware import csrf
from django.template import RequestContext
from django.core.paginator import Paginator
# Create your views here.

def register(request):
    # sys_messages = messages.get_messages(request)
    # for message in sys_messages:
    #     pass
    #sys_messages.used = True
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            print ('takeb')
            return redirect('/register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            print ('takeb')
            return redirect('/register')
        else:
            user = User.objects.create_user(username=username,password=password,email=email)
            user.save()
            print("user created successfully please login")
            return redirect('/')
    else:
        pass
    return render(request, 'register.html')

def login(request):
    c={}
    #c.update(csrf(request))
    if request.user.is_authenticated:
        return redirect('/welcome')
    else:
        c={}
        #c.update(csrf(request))
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/welcome')

            else:
                messages.info(request, 'Username or Password does not match')
                return redirect('/')

        else:
            pass
    return render(request, 'login.html') 


def logouts(request):
    messages.info(request, 'Log Out Successful')
    logout(request)
    return redirect('/')


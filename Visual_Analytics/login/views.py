
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.core.mail import send_mail
from .email import send_forget_password_mail
from django.contrib import messages
import datetime
import re
from .token import generate_token




x = datetime.datetime.now()

dtstamp=x.strftime("%c")


def home(request):
    global token
    token= generate_token(10)
    list={'token':token,'dt':dtstamp}
    return render(request,'login.html',context=list)

# def log(request,token):
#
#     return render(request,'dashboard.html')


def login(request,token):
    try:
        if request.method=='POST':
            global email
            email = request.POST.get('email')
            ps= request.POST.get('password')
            user=authenticate(request,username=email, password=ps)
            valid = User.objects.filter(username=email).exists()

            if user is not None:
                auth_login(request,user)
                shared_variable = email
                request.session['shared_variable'] = shared_variable

                return redirect(f'/log/{token}')
            elif email=="" and ps=="":
                messages.success(request, 'both field required')
                return redirect('/')
            elif valid == False:
                messages.success(request, 'Not user found with this username.')
                return redirect('/')
            else:
                messages.success(request, 'Enter valid username and password.')
                return redirect('/')
    except Exception as e:
        print(e)

def forgot(request):
    return render(request, 'forgot.html')

def ChangePassword(request,id):
    print(request.method)

    try:

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            pattern = ("^.*(?=.{6,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$")
            result = re.findall(pattern, new_password)

            print(new_password,confirm_password )

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/newpass/{id}')


            if not (result):
                messages.success(request, 'use strong pass')
                return redirect(f'/newpass/{id}')

            else:
                user_obj = User.objects.get(id=id)
                user_obj.set_password(new_password)
                user_obj.save()
                return redirect('/')

    except Exception as e:
        print(e)


def changepass(request):
    return render(request, 'html/changepass.html')

def ForgetPassword(request):

    try:
        if request.method == 'POST':
            username = request.POST.get('email')

            user=User.objects.filter(username=username).exists()
            id = User.objects.filter(username=username).values_list('id', flat=True).first()
            super = User.objects.filter(username=username).values_list('is_superuser', flat=True).first()
            print(id,super)
            if user==False:
                messages.success(request, 'Not user found with this username.')
                return redirect('/forgot/',{'id':id})
            if super == False:
                messages.success(request, 'access denied')
                return redirect('/forgot/',{'id':id})
            if user != False and super != False:
                user_obj = User.objects.get(username=username)
                send_forget_password_mail(user_obj, id)
                messages.success(request, 'Mail send to register mail ID')
                return redirect('/forgot/')




    except Exception as e:
        print(e)


#
def newpass(request,id):
    return render(request, 'change.html',{'id':id})

from django.shortcuts import render

# Create your views here.


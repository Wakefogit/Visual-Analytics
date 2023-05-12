from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.core.mail import send_mail
from .email  import send_forget_password_mail



from django.contrib import messages




def home(request):
    return render(request,'login.html')

def log(request):
    return render(request,'dashboard.html')


def login(request):
    if request.method=='POST':

        email = request.POST.get('email')
        ps= request.POST.get('password')
        user=authenticate(request,username=email, password=ps)

        if user is not None:
            auth_login(request, user)
            return redirect('/log/')
        else:
            return HttpResponse ("user not found")

def forgot(request):
    return render(request, 'forgot.html')

def ChangePassword(request,id):
    print("ok")


    try:

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            print(new_password,confirm_password )

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect("/newpass/")

            user_obj = User.objects.get(id=id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/')

    except Exception as e:
        print(e)


def changepass(request):
    return render(request, 'html/changepass.html')

def ForgetPassword(request):
    print(request.method)

    try:
        if request.method == 'POST':
            username = request.POST.get('email')

            user=User.objects.filter(username=username).exists()
            id = User.objects.filter(username=username).values_list('id', flat=True).first()




            if user==False:
                messages.success(request, 'Not user found with this username.')
                return redirect('/forgot/',{'id':id})

            user_obj = User.objects.get(username=username)

            send_forget_password_mail(user_obj, id)




    except Exception as e:
        print(e)


    messages.success(request, 'Mail send to register mail ID')
    return redirect('/forgot/')
#
def newpass(request,id):
    return render(request, 'change.html',{'id':id})
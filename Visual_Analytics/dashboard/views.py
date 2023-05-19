from django.shortcuts import render

# Create your views here.
from .models import helmet_detection
from .token import generate_token


def log(request,token):
    global token1
    token1 = generate_token(10)
    list={'token1':token1}

    return render(request,'dashboard.html',context=list)

def table(request,token1):
    table=helmet_detection.objects.all()
    list={"table":table}
    return render(request,"reports.html",context=list)


# Create your views here.


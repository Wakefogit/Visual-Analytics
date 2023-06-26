from django.shortcuts import render,redirect
from django.http import HttpResponse
# from ..login.views import *
from django.db.models import Max
from functools import reduce
from django.contrib.auth.models import User
# from login.views import email
from .models import helmet_detection,final_report
from .token import generate_token


def log(request,token):
    global token1

    shared_variable = request.session.get('shared_variable')
    username = User.objects.filter(username = shared_variable ).values_list('first_name', flat=True).first()
    max_id = helmet_detection.objects.count()
    token1 = generate_token(10)
    list = {'token1':token1,"max_id":max_id ,"username":username}
    return render(request, 'dashboard.html', context=list)

def table(request,token1):
    table = helmet_detection.objects.all()
    list = {"table":table,'token1':token1}
    return render(request, "helmet_detection.html", context=list)

def submit(request,violation_id,token1):
    if request.method == 'POST':
        remark = reduce(lambda x, y: x + y, request.POST.getlist('remark'))
        msg = reduce(lambda x, y: x + y, request.POST.getlist('msg'))
        helmet_detection.objects.filter(violation_id=violation_id).update(supervisor_remark=remark, message=msg)
        row = helmet_detection.objects.get(violation_id=violation_id)
        new_row = final_report()
        new_row.violation_type = row.violation_type
        new_row.time_stamp = row.time_stamp
        new_row.camera_number = row.camera_number
        new_row.supervisor_remark = remark
        new_row.artefact = row.artefact
        new_row.message = msg
        new_row.save()
        row.delete()
        table = helmet_detection.objects.all()
        list = {"table":table,'token1':token1}
        return redirect(f'/table/{token1}',context=list)

        # return render(request, "helmet_detection.html", context=list)
    else:
        return HttpResponse("no")


def report(request,token1):
    table1 = final_report.objects.all()
    print(table)
    list = {"table": table1, 'token1': token1}
    return render(request, "report.html", context=list)

from django.shortcuts import render,redirect
from django.http import HttpResponse
# from ..login.views import *
from django.db.models import Max
from functools import reduce
from django.contrib.auth.models import User
# from login.views import email
from .models import helmet_detection,final_report,hazard_protection,vehicle_speed,billet
from .token import generate_token
from django.db import models
from django.db.models.functions import Cast, Trunc
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from django.contrib import messages




def fetch_last_5_records():
    all_records = []
    all_records.extend(helmet_detection.objects.order_by('-time_stamp')[:5])
    all_records.extend(vehicle_speed.objects.order_by('-time_stamp')[:5])
    all_records.extend(hazard_protection.objects.order_by('-time_stamp')[:5])
    all_records.extend(billet.objects.order_by('-time_stamp')[:5])

    # Sorting the records based on time_stamp in descending order
    sorted_records = sorted(all_records, key=lambda record: record.time_stamp, reverse=True)
    global last_5_records
    # Retrieving the last 5 records without loop
    last_5_records = sorted_records[:5]

    # Fetch the last 5 records for violation_type and time_stamp
    # global last_5_records
    # last_5_records = helmet_detection.objects.order_by('-time_stamp').values('violation_type', 'time_stamp')[:5]




def log(request,token):

    fetch_last_5_records()
    global t
    t=token
    global token1
    shared_variable = request.session.get('shared_variable')
    global username
    username = User.objects.filter(username = shared_variable ).values_list('first_name', flat=True).first()
    global max_id
    max_id1 = helmet_detection.objects.count()
    max_id2 = hazard_protection.objects.count()
    max_id3 = vehicle_speed.objects.count()
    max_id4 = billet.objects.count()
    max_id=[max_id1,max_id2,max_id3,max_id4]
    token1 = generate_token(10)
    list = {'token1':token1,"max_id":max_id ,"username":username ,token:"token","token":t ,"last_5_records":last_5_records ,"active":"active"}
    return render(request, 'dashboard.html', context=list)

def helmet(request,token1):
    table = helmet_detection.objects.all()
    title= "Hemlet Detection"
    list = {"table":table,'token1':token1, "username":username,"title":title,"last_5_records":last_5_records,"active":"active"}
    return render(request,"popup.html", context=list)

def Hazard_Protection(request,token1):
    table = hazard_protection.objects.all()
    title= "HazardProtection"
    list = {"table":table,'token1':token1, "username":username ,"title":title,"last_5_records":last_5_records,"active":"active"}
    return render(request,"popup.html", context=list)

def vehicle(request,token1):
    table = vehicle_speed.objects.all()
    title= "Vehicle Speed"
    list = {"table":table,'token1':token1, "username":username ,"title":title,"last_5_records":last_5_records,"active":"active"}
    return render(request,"popup.html", context=list)

def Double_billet(request,token1):
    table = billet.objects.all()
    title= "Double Billet"
    list = {"table":table,'token1':token1, "username":username ,"title":title,"last_5_records":last_5_records,"active":"active"}
    return render(request,"popup.html", context=list)


def submit(request,violation_id,token1,violation_type):
    print(type(violation_type),violation_type)
    if request.method == 'POST':
        remark = reduce(lambda x, y: x + y, request.POST.getlist('remark'))
        msg = reduce(lambda x, y: x + y, request.POST.getlist('msg'))
        if violation_type == "NO_helmet":
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
            list = {"table": table, 'token1': token1, "token": t, "username": username, "helmet": helmet,
                    "last_5_records": last_5_records}
            return render(request, "popup.html", context=list)


        elif violation_type == "hazard_protection":
            hazard_protection.objects.filter(violation_id=violation_id).update(supervisor_remark=remark, message=msg)
            row = hazard_protection.objects.get(violation_id=violation_id)
            new_row = final_report()
            new_row.violation_type = row.violation_type
            new_row.time_stamp = row.time_stamp
            new_row.camera_number = row.camera_number
            new_row.supervisor_remark = remark
            new_row.artefact = row.artefact
            new_row.message = msg
            new_row.save()
            row.delete()
            table = hazard_protection.objects.all()
            list = {"table": table, 'token1': token1, "token": t, "username": username, "helmet": helmet,
                    "last_5_records": last_5_records}
            return render(request, "popup.html", context=list)
        elif violation_type == "Vehicle_Speed":
            vehicle_speed.objects.filter(violation_id=violation_id).update(supervisor_remark=remark, message=msg)
            row = vehicle_speed.objects.get(violation_id=violation_id)
            new_row = final_report()
            new_row.violation_type = row.violation_type
            new_row.time_stamp = row.time_stamp
            new_row.camera_number = row.camera_number
            new_row.supervisor_remark = remark
            new_row.artefact = row.artefact
            new_row.message = msg
            new_row.save()
            row.delete()
            table = vehicle_speed.objects.all()
            list = {"table": table, 'token1': token1, "token": t, "username": username, "helmet": helmet,
                    "last_5_records": last_5_records}
            return render(request, "popup.html", context=list)
        elif violation_type == "double Billet":
            billet.objects.filter(violation_id=violation_id).update(supervisor_remark=remark, message=msg)
            row = billet.objects.get(violation_id=violation_id)
            new_row = final_report()
            new_row.violation_type = row.violation_type
            new_row.time_stamp = row.time_stamp
            new_row.camera_number = row.camera_number
            new_row.supervisor_remark = remark
            new_row.artefact = row.artefact
            new_row.message = msg
            new_row.save()
            row.delete()
            table = billet.objects.all()
            list = {"table": table, 'token1': token1, "token": t, "username": username, "helmet": helmet,
                    "last_5_records": last_5_records}
            return render(request, "popup.html", context=list)



    else:
        return HttpResponse("No Record")


def report(request,token1):
    fetch_last_5_records()
    table= final_report.objects.all()
    list = {"table": table, 'token1': token1 , "username":username ,"last_5_records":last_5_records,"token":t,"active1":"active"}
    return render(request, "report.html", context=list)


# def filter_table(request,token1):
#     if request.method == 'POST':
#         # Get the checkbox values
#         global violation_types
#         violation_types = request.POST.getlist('violation_type')
#         print(violation_types)
#
#
#         if 'All' in violation_types:
#             table_data = final_report.objects.all()
#         else:
#             table_data = final_report.objects.filter(violation_type__in=violation_types)
#
#         list = {"table": table_data, 'token1': token1, "username": username, "last_5_records": last_5_records,
#                 "token": t}
#         return render(request, "report.html", context=list)

def filter_report(request,token1):
    try:
        if request.method == 'POST':
            global start_date
            global end_date
            global violation_types
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            violation_types = request.POST.getlist('violation_type')

            # Filter the report table based on start and end dates

            filtered_records = final_report.objects.filter(
                time_stamp__date__gte=start_date,
                time_stamp__date__lte=end_date,
                violation_type__in=violation_types
            )
            # filtered_records = final_report.objects.filter(
            #     time_stamp__date__gte=start_date,
            #     time_stamp__date__lte=end_date
            # )
            # filtered_data = final_report.objects.filter(date__range=[start_date, end_date])
            list = {"table": filtered_records , 'token1': token1, "username":username ,"last_5_records":last_5_records,"token":t}
            return render(request, "report.html",context=list)
    except:
        table = final_report.objects.all()
        messages.success(request, 'start date and end date required')
        list = {'token1': token1, "username": username, "last_5_records": last_5_records, "token": t,"table":table}
        return render(request, "report.html", context=list)


def download_pdf(request):
    try:
        data = final_report.objects.filter(
            time_stamp__date__gte=start_date,
            time_stamp__date__lte=end_date,
            violation_type__in=violation_types
        ).annotate(
            formatted_time_stamp=Cast(Trunc('time_stamp', 'second'), output_field=models.DateTimeField())
        ).values_list(
            'violation_id',
            'violation_type',
            'formatted_time_stamp',
            'camera_number',
            'supervisor_remark',
            'message'
        )


        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report {start_date}-{end_date}.pdf"'

        # Create a PDF document
        pdf = SimpleDocTemplate(response, pagesize=letter)

        # Create a list to hold elements of the document
        elements = []

        # Add the company logo, title, and timestamp
        logo_path = 'static/img/logo.png'  # Replace with the actual path to the logo file
        logo = Image(logo_path, width=1.7 * inch, height=0.5* inch)  # Adjust the width and height as needed
        elements.append(logo)

        title_style = getSampleStyleSheet()['Title']
        title_text = f'<H3>REPORT</H3>'
        title = Paragraph(title_text, title_style)
        elements.append(title)

        timestamp_style = getSampleStyleSheet()['Normal']
        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp_text = f'Time: {current_timestamp}  <br/>   SD : {start_date}  -   ED : {end_date}'
        timestamp = Paragraph(timestamp_text, timestamp_style)
        elements.append(timestamp)

        elements.append(Spacer(1, 0.5 * inch))  # Add some space between elements

        # Add the table headers


        table_data = [
            ['Violation ID', 'Violation Type', 'Timestamp', 'Camera Number', 'Supervisor Remark', 'Message']
        ]

        # Add table rows
        for row in data:
            table_data.append(list(row))

        # Define table style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Create the table and apply the style
        table = Table(table_data)
        table.setStyle(table_style)

        # Add the table to the elements
        elements.append(table)

        # Build the PDF document with the elements
        pdf.build(elements)

        return response
    except:
        return HttpResponse ("<H4>start date and end date required</H4>")


def live(request, token1):
        list = {'token1': token1, "username": username, "last_5_records": last_5_records, "token": t,"active4":"active"}
        return render(request, "user_management.html", context=list)

    # rtsp_stream_url = 'rtsp://admin:Admin@1234@192.168.1.64/doc/page/preview.asp'
    # http_stream_url = 'http://127.0.0.1:8080/live'  # Use the desired URL for the converted HTTP stream

    # context = {'token1': token1, "username": username, "last_5_records": last_5_records, "token": t, "active3": "active", "rtsp_stream_url": rtsp_stream_url, "http_stream_url": http_stream_url}
    # return render(request, "user_management.html", context=context)

# def user_management(request,token1):
#     list = {'token1': token1, "username": username, "last_5_records": last_5_records, "token": t,"active4":"active"}
#     return render(request, "user_management.html", context=list)

def camera_management(request,token1):
    list = {'token1': token1, "username": username, "last_5_records": last_5_records, "token": t,"active2":"active"}
    return render(request, "camera_management.html", context=list)




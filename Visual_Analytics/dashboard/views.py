from django.shortcuts import render,redirect
from django.http import HttpResponse
# from ..login.views import *
from django.db.models import Max
from functools import reduce
from django.contrib.auth.models import User
# from login.views import email
from .models import helmet_detection,final_report
from .token import generate_token
from django.db import models
from django.db.models.functions import Cast, Trunc
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

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
        return HttpResponse("No Record")


def report(request,token1):
    table1 = final_report.objects.all()
    print(table)
    list = {"table": table1, 'token1': token1}
    return render(request, "report.html", context=list)

def filter_report(request,token1):
    print(request,'test')
    if request.method == 'POST':
        global start_date
        global end_date
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        print(start_date,end_date)

        # Filter the report table based on start and end dates
        filtered_records = final_report.objects.filter(
            time_stamp__date__gte=start_date,
            time_stamp__date__lte=end_date
        )
        # filtered_data = final_report.objects.filter(date__range=[start_date, end_date])
        list = {"table": filtered_records , 'token1': token1}
        return render(request, "report.html",context=list)



def download_pdf(request):

    data = final_report.objects.filter(
        time_stamp__date__gte=start_date,
        time_stamp__date__lte=end_date
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

# def download_pdf(request):
#     data = final_report.objects.filter(
#             time_stamp__date__gte=start_date,
#             time_stamp__date__lte=end_date
#         ).values_list(
#         'violation_id',
#         'violation_type',
#         'time_stamp',
#         'camera_number',
#         'supervisor_remark',
#         'message'
#     )
#
#     # Create a PDF response
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="table_data.pdf"'
#
#     # Create a PDF document
#     pdf = SimpleDocTemplate(response, pagesize=letter)
#
#     # Create a list to hold table data
#     table_data = []
#
#     # Add table headers
#     table_data.append(
#         ['Violation ID', 'Violation Type', 'Timestamp', 'Camera Number', 'Supervisor Remark', 'Message'])
#
#     # Add table rows
#     for row in data:
#         table_data.append(list(row))
#
#     # Define table style
#     table_style = TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 8),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ])
#
#     # Create the table and apply the style
#     table = Table(table_data)
#     table.setStyle(table_style)
#
#     # Build the PDF document and render the table
#     elements = [table]
#     pdf.build(elements)
#     print('done !')
#     return response
#     # return HttpResponse("done !")
#






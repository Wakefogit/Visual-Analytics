"""
URL configuration for Visual_Analytics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboard import views
urlpatterns = [
    # path("admin/", admin.site.urls),
    path('helmet/<token1>', views.helmet),
    path('Hazard/<token1>', views.Hazard_Protection),
    path('vehicle/<token1>', views.vehicle),
    path('Double_billet/<token1>', views.Double_billet),
    path("log/<token>", views.log),
    path("submit/<token1>/<violation_id>/<violation_type>", views.submit),
    path('report/<token1>', views.report),
    path('filter_report/<token1>', views.filter_report),
    # path('filter_table/<token1>', views.filter_table),
    path('download/', views.download_pdf),
    path('report/<token1>/<start_date>/<end_date>', views.report),
    # path("log/alert", views.alert),
    path("live/<token1>", views.live),
    path("camera_management/<token1>", views.camera_management),

]
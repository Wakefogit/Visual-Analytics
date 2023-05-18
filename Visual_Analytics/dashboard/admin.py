from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import helmet_detection


class productAdmin(admin.ModelAdmin):
    list_display = ["violation_id","violation_type","time_stamp","camera_number","supervisor_remark","artefact","message"]


admin.site.register(helmet_detection, productAdmin)
from django.contrib import admin

# Register your models here.

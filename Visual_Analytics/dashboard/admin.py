from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import helmet_detection,final_report


class productAdmin(admin.ModelAdmin):
    list_display = ["violation_id","violation_type","time_stamp","camera_number","supervisor_remark","artefact","message"]


admin.site.register(helmet_detection, productAdmin)


class report(admin.ModelAdmin):
    class Meta:
        model = final_report

admin.site.register(final_report,report)

# Register your models here.

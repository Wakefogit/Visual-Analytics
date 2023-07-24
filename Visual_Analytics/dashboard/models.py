from django.db import models
from datetime import datetime

class BaseViolation(models.Model):
    violation_id = models.AutoField(primary_key=True)
    violation_type = models.CharField(max_length=20)
    time_stamp = models.DateTimeField(default=datetime.now)
    camera_number = models.CharField(max_length=20)
    supervisor_remark = models.CharField(max_length=50, null=False)
    artefact = models.ImageField(upload_to="result/")
    message = models.CharField(max_length=50, null=False)

    class Meta:
        abstract = True

class helmet_detection(BaseViolation):
    pass
    # Additional fields specific to HelmetDetection model

class final_report(BaseViolation):
    pass
    # Additional fields specific to FinalReport model

class vehicle_speed(BaseViolation):
    pass
    # Additional fields specific to VehicleSpeed model


class hazard_protection(BaseViolation):
    pass
    # Additional fields specific to HazardProtection model
class billet(BaseViolation):
    pass
    # Additional fields specific to HazardProtection model


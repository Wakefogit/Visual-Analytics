from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime
# Create your models here.
from django.db import models

# Create your models here.
class helmet_detection(models.Model):
    violation_id = models.AutoField(primary_key=True)
    violation_type = models.CharField(max_length=20)
    time_stamp = models.DateTimeField(default=datetime.now)
    camera_number = models.CharField(max_length=20)
    supervisor_remark = models.CharField(max_length=50)
    artefact = models.ImageField(upload_to="C:\\Users\\LENOVO\\PycharmProjects\\Visual-Analytics\\Visual_Analytics\\output")
    message = models.CharField(max_length=50)


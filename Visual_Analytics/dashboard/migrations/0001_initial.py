# Generated by Django 4.2.3 on 2023-07-20 11:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="billet",
            fields=[
                ("violation_id", models.AutoField(primary_key=True, serialize=False)),
                ("violation_type", models.CharField(max_length=20)),
                ("time_stamp", models.DateTimeField(default=datetime.datetime.now)),
                ("camera_number", models.CharField(max_length=20)),
                ("supervisor_remark", models.CharField(max_length=50)),
                ("artefact", models.ImageField(upload_to="result/")),
                ("message", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="final_report",
            fields=[
                ("violation_id", models.AutoField(primary_key=True, serialize=False)),
                ("violation_type", models.CharField(max_length=20)),
                ("time_stamp", models.DateTimeField(default=datetime.datetime.now)),
                ("camera_number", models.CharField(max_length=20)),
                ("supervisor_remark", models.CharField(max_length=50)),
                ("artefact", models.ImageField(upload_to="result/")),
                ("message", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="hazard_protection",
            fields=[
                ("violation_id", models.AutoField(primary_key=True, serialize=False)),
                ("violation_type", models.CharField(max_length=20)),
                ("time_stamp", models.DateTimeField(default=datetime.datetime.now)),
                ("camera_number", models.CharField(max_length=20)),
                ("supervisor_remark", models.CharField(max_length=50)),
                ("artefact", models.ImageField(upload_to="result/")),
                ("message", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="helmet_detection",
            fields=[
                ("violation_id", models.AutoField(primary_key=True, serialize=False)),
                ("violation_type", models.CharField(max_length=20)),
                ("time_stamp", models.DateTimeField(default=datetime.datetime.now)),
                ("camera_number", models.CharField(max_length=20)),
                ("supervisor_remark", models.CharField(max_length=50)),
                ("artefact", models.ImageField(upload_to="result/")),
                ("message", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="vehicle_speed",
            fields=[
                ("violation_id", models.AutoField(primary_key=True, serialize=False)),
                ("violation_type", models.CharField(max_length=20)),
                ("time_stamp", models.DateTimeField(default=datetime.datetime.now)),
                ("camera_number", models.CharField(max_length=20)),
                ("supervisor_remark", models.CharField(max_length=50)),
                ("artefact", models.ImageField(upload_to="result/")),
                ("message", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]

# Generated by Django 3.2.8 on 2022-08-23 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linebotApp', '0010_job_hunting_id_alter_job_hunting_lineid'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='job_type',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='company',
            name='welfare',
            field=models.CharField(default='', max_length=255),
        ),
    ]

# Generated by Django 3.2.6 on 2021-11-20 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bootcamps', '0002_bootcamp_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bootcamp',
            name='average_rating',
        ),
    ]
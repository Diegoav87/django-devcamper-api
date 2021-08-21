# Generated by Django 3.2.6 on 2021-08-13 14:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Bootcamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(max_length=500)),
                ('website', models.URLField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$', message="The phone number should be in format: '+999999999'. Up to 15 digits allowed")])),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('average_rating', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])),
                ('housing', models.BooleanField(default=False)),
                ('job_assistance', models.BooleanField(default=False)),
                ('job_guarantee', models.BooleanField(default=False)),
                ('accept_gi', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('careers', models.ManyToManyField(blank=True, to='bootcamps.Career')),
            ],
        ),
    ]

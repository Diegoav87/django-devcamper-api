# Generated by Django 3.2.6 on 2021-12-19 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='weeks',
            field=models.IntegerField(),
        ),
    ]

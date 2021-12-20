# Generated by Django 3.2.6 on 2021-12-20 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bootcamps', '0003_remove_bootcamp_average_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='bootcamp',
            name='lat',
            field=models.DecimalField(decimal_places=6, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='bootcamp',
            name='lng',
            field=models.DecimalField(decimal_places=6, max_digits=8, null=True),
        ),
    ]
from django.contrib import admin
from .models import Bootcamp, Career
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.


@admin.register(Bootcamp)
class BootcampAdmin(OSMGeoAdmin):
    list_display = ('name',)


admin.site.register(Career)

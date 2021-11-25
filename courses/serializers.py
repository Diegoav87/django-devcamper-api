from rest_framework import serializers

from .models import Course
from bootcamps.serializers import BootcampSimpleSerializer
from bootcamps.serializers import DynamicFieldsModelSerializer


class CourseSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    bootcamp = BootcampSimpleSerializer(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

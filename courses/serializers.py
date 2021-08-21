from rest_framework import serializers

from .models import Course
from bootcamps.serializers import BootcampListSerializer
from bootcamps.serializers import DynamicFieldsModelSerializer


class CourseSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    bootcamp = BootcampListSerializer(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

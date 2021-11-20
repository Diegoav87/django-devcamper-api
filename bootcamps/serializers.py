from rest_framework import serializers

from .models import Bootcamp, Career
from courses.models import Course
from accounts.serializers import CustomUserSerializer


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ('name',)


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'description', 'weeks')


class BootcampSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    careers = CareerSerializer(read_only=True, many=True)
    user = CustomUserSerializer(read_only=True)
    courses = CourseListSerializer(read_only=True, many=True)

    class Meta:
        model = Bootcamp
        fields = '__all__'


class BootcampListSerializer(DynamicFieldsModelSerializer, serializers.ModelSerializer):
    careers = CareerSerializer(read_only=True, many=True)
    average_cost = serializers.IntegerField()
    average_rating = serializers.IntegerField()

    class Meta:
        model = Bootcamp
        fields = ("name", "careers", "photo", "average_cost", "average_rating")

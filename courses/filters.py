import django_filters

from .models import Course


class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
            'weeks': ['exact'],
            'tuition': ['exact'],
            'minimum_skill': ['exact'],
            'scolarship_available': ['exact']
        }

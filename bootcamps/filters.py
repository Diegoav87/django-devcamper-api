import django_filters

from .models import Bootcamp


class BootcampFilter(django_filters.FilterSet):
    class Meta:
        model = Bootcamp
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'housing': ['exact'],
            'job_assistance': ['exact'],
            'job_guarantee': ['exact'],
            'accept_gi': ['exact']
        }

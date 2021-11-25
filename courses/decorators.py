from rest_framework.response import Response
from .models import Course
from rest_framework import status
from bootcamps.models import Bootcamp


def course_exists(view_func):
    def wrapper_func(request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            course = Course.objects.get(id=pk)
            return view_func(request, *args, **kwargs)
        except Course.DoesNotExist:
            return Response(f"Course with ID of {pk} does not exist", status=status.HTTP_404_NOT_FOUND)
    return wrapper_func


def course_write_permission(view_func):
    def wrapper_func(request, *args, **kwargs):
        pk = kwargs.get('pk')
        course = Course.objects.get(id=pk)

        if course.bootcamp.user != request.user:
            return Response("You are not authorized to perform this action", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

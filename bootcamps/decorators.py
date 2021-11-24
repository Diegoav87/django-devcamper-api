from rest_framework.response import Response
from .models import Bootcamp
from rest_framework import status


def bootcamp_exists(view_func):
    def wrapper_func(request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            bootcamp = Bootcamp.objects.get(id=int(pk))
            return view_func(request, *args, **kwargs)
        except Bootcamp.DoesNotExist:
            return Response(f"Bootcamp with ID of {pk} does not exist", status=status.HTTP_404_NOT_FOUND)
    return wrapper_func


def bootcamp_write_permission(view_func):
    def wrapper_func(request, *args, **kwargs):
        pk = kwargs.get('pk')
        bootcamp = Bootcamp.objects.get(id=pk)

        if bootcamp.user != request.user:
            return Response("You are not authorized to perform this action", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

from rest_framework.response import Response
from rest_framework import status
from .models import Review


def review_exists(view_func):
    def wrapper_func(request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            review = Review.objects.get(id=pk)
            return view_func(request, *args, **kwargs)
        except Review.DoesNotExist:
            return Response(f"Review with ID of {pk} does not exist", status=status.HTTP_404_NOT_FOUND)
    return wrapper_func


def review_write_permission(view_func):
    def wrapper_func(request, *args, **kwargs):
        pk = kwargs.get('pk')
        review = Review.objects.get(id=pk)

        if review.user != request.user:
            return Response("You are not authorized to perform this action", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

from rest_framework.response import Response
from rest_framework import status


def sort_queryset(queryset, sort):
    new_queryset = queryset

    if sort != '':
        try:
            new_queryset = queryset.order_by(sort)
        except:
            return Response("Sorting query does not exist", status=status.HTTP_400_BAD_REQUEST)

    return new_queryset

from django.shortcuts import render

from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination

from .serializers import BootcampSerializer
from .models import Bootcamp, Career
from .decorators import bootcamp_exists, bootcamp_write_permission
from .filters import BootcampFilter
from utils.sort import sort_queryset
from utils.select import select_fields

# Create your views here.


@api_view(['GET'])
def get_bootcamps(request):
    bootcamps = Bootcamp.objects.all()

    # Filter
    bootcamp_filter = BootcampFilter(request.GET, queryset=bootcamps)
    bootcamps = bootcamp_filter.qs

    # Sort
    sort = request.GET.get('sort', '')

    bootcamps = sort_queryset(bootcamps, sort)

    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10
    bootcamps = paginator.paginate_queryset(bootcamps, request)

    # Select
    fields = request.GET.get('fields', '')

    serializer = select_fields(BootcampSerializer, bootcamps, fields)

    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@bootcamp_exists
def get_bootcamp(request, pk):
    bootcamp = Bootcamp.objects.get(id=pk)
    serializer = BootcampSerializer(bootcamp)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_bootcamp(request):
    serializer = BootcampSerializer(data=request.data)

    if serializer.is_valid():
        bootcamp = serializer.save(user=request.user)

        careers = request.data.get('careers', '')

        if careers != '':
            for career in careers:
                career_obj = Career.objects.get(name=career)
                bootcamp.careers.add(career_obj)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@bootcamp_exists
@bootcamp_write_permission
def update_bootcamp(request, pk):
    bootcamp = Bootcamp.objects.get(id=pk)
    serializer = BootcampSerializer(
        instance=bootcamp, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@bootcamp_exists
@bootcamp_write_permission
def delete_bootcamp(request, pk):
    bootcamp = Bootcamp.objects.get(id=pk)
    bootcamp.delete()
    return Response("Bootcamp deleted", status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
@bootcamp_exists
@bootcamp_write_permission
def upload_photo(request, pk):
    bootcamp = Bootcamp.objects.get(id=pk)
    image = request.data.get('image', '')

    if image == '':
        return Response("There was no image attached in the request", status=status.HTTP_400_BAD_REQUEST)

    bootcamp.photo = image
    bootcamp.save()
    return Response("Your image was uploaded", status=status.HTTP_200_OK)

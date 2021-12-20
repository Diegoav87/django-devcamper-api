from django.shortcuts import render, get_object_or_404
from django.db.models import Avg

from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser
from rest_framework.pagination import PageNumberPagination
from geopy.geocoders import Nominatim

from .serializers import BootcampSerializer, BootcampListSerializer, BootcampCreateSerializer
from .models import Bootcamp, Career
from .decorators import bootcamp_exists, bootcamp_write_permission
from .filters import BootcampFilter
from utils.sort import sort_queryset
from utils.select import select_fields
from utils.geolocation import geolocate, haversine, calculate_distance

# Create your views here.

geolocator = Nominatim(user_agent="geopiExercises")


@api_view(['GET'])
def get_bootcamps(request):
    bootcamps = Bootcamp.objects.annotate(average_cost=Avg(
        "courses__tuition"), average_rating=Avg("reviews__rating"))

    average_rating = request.GET.get("average_rating", "")
    average_cost = request.GET.get("average_cost", "")
    career = request.GET.get("career", "")

    # Filter
    bootcamp_filter = BootcampFilter(request.GET, queryset=bootcamps)
    bootcamps = bootcamp_filter.qs

    if average_rating != "":
        bootcamps = bootcamps.filter(average_rating__gte=int(average_rating))

    if average_cost != "":
        bootcamps = bootcamps.filter(average_cost__lte=int(average_cost))

    if career != "":
        career = Career.objects.get(name=career)
        bootcamps = bootcamps.filter(careers__in=[career.id])

    # Sort
    sort = request.GET.get('sort', '')

    bootcamps = sort_queryset(bootcamps, sort)

    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 5
    bootcamps = paginator.paginate_queryset(bootcamps, request)

    # Select
    fields = request.GET.get('fields', '')

    serializer = select_fields(BootcampListSerializer, bootcamps, fields)

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def get_latest_bootcamps(request):
    bootcamps = Bootcamp.objects.annotate(average_cost=Avg(
        "courses__tuition"), average_rating=Avg("reviews__rating")).order_by('-created_at')[:3]
    serializer = BootcampListSerializer(bootcamps, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@bootcamp_exists
def get_bootcamp(request, pk):
    bootcamp = Bootcamp.objects.annotate(average_cost=Avg(
        "courses__tuition"), average_rating=Avg("reviews__rating")).get(id=pk)
    serializer = BootcampSerializer(bootcamp)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_bootcamp_for_user(request):
    try:
        bootcamp = Bootcamp.objects.annotate(average_cost=Avg(
            "courses__tuition"), average_rating=Avg("reviews__rating")).get(user=request.user)
    except Bootcamp.DoesNotExist:
        return Response("Bootcamp for user does not exist", status=status.HTTP_404_NOT_FOUND)

    serializer = BootcampSerializer(bootcamp)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_bootcamp(request):
    serializer = BootcampCreateSerializer(data=request.data)

    if serializer.is_valid():
        address = serializer.validated_data['address']
        point = geolocate(address)

        if point == None:
            return Response("Please enter a valid address", status=status.HTTP_400_BAD_REQUEST)

        bootcamp = serializer.save(
            user=request.user, lng=point[0], lat=point[1])

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
    serializer = BootcampCreateSerializer(
        instance=bootcamp, data=request.data, partial=True)

    if serializer.is_valid():
        address = serializer.validated_data['address']
        point = ''

        if address != bootcamp.address:
            point = geolocate(address)

            if point == None:
                return Response("Please enter a valid address", status=status.HTTP_400_BAD_REQUEST)

        bootcamp = ''
        if point != "":
            bootcamp = serializer.save(lng=point[0], lat=point[1])
        else:
            bootcamp = serializer.save()

        careers = request.data.get('careers', '')

        if careers != '':
            bootcamp.careers.clear()

            for career in careers:
                career_obj = Career.objects.get(name=career)
                bootcamp.careers.add(career_obj)

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


@api_view(['GET'])
def get_bootcamps_within_radius(request, km, zipcode):
    location = geolocator.geocode(zipcode)

    if location == None:
        return Response("There were no results for your zipcode", status=status.HTTP_400_BAD_REQUEST)

    center_point = (location.latitude, location.longitude)

    bootcamps = Bootcamp.objects.all()

    in_radius_bootcamps = []

    for bootcamp in bootcamps:
        test_point = (bootcamp.lat, bootcamp.lng)
        if calculate_distance(center_point, test_point, km):
            in_radius_bootcamps.append(bootcamp.name)

    bootcamps = Bootcamp.objects.annotate(average_cost=Avg(
        "courses__tuition"), average_rating=Avg("reviews__rating")).filter(name__in=in_radius_bootcamps)
    serializer = BootcampListSerializer(bootcamps, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

from django.shortcuts import render
from django.db.models import Avg

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .serializers import CourseSerializer
from bootcamps.decorators import bootcamp_exists, bootcamp_write_permission
from bootcamps.models import Bootcamp
from .models import Course
from .decorators import course_exists, course_write_permission
from .filters import CourseFilter
from utils.sort import sort_queryset
from utils.select import select_fields

# Create your views here.


@api_view(['GET'])
def get_courses(request):
    courses = Course.objects.all()

    # Filter
    course_filter = CourseFilter(request.GET, queryset=courses)
    courses = course_filter.qs

    # Sort
    sort = request.GET.get('sort', '')
    courses = sort_queryset(courses, sort)

    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10
    courses = paginator.paginate_queryset(courses, request)

    # Select
    fields = request.GET.get('fields', '')

    serializer = select_fields(CourseSerializer, courses, fields)

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@course_exists
def get_course(request, pk):
    course = Course.objects.get(id=pk)
    serializer = CourseSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@bootcamp_exists
@bootcamp_write_permission
def create_course(request, pk):
    bootcamp = Bootcamp.objects.get(id=pk)
    serializer = CourseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(bootcamp=bootcamp)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@course_exists
@course_write_permission
def update_course(request, pk):
    course = Course.objects.get(id=pk)
    serializer = CourseSerializer(
        instance=course, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@course_exists
@course_write_permission
def delete_course(request, pk):
    course = Course.objects.get(id=pk)
    course.delete()
    return Response("Course deleted", status=status.HTTP_200_OK)

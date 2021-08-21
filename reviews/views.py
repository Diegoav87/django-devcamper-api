from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ReviewSerializer
from .models import Review
from bootcamps.models import Bootcamp
from bootcamps.decorators import bootcamp_exists
from .decorators import review_exists, review_write_permission

# Create your views here.


@api_view(['GET'])
@bootcamp_exists
def get_bootcamp_reviews(request, pk):
    bootcamp = Bootcamp.objects.get(id=pk)
    serializer = ReviewSerializer(bootcamp.reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@bootcamp_exists
def add_review(request, pk):
    bootcamp = Bootcamp.objects.get(id=pk)
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user, bootcamp=bootcamp)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@review_exists
@review_write_permission
def update_review(request, pk):
    review = Review.objects.get(id=pk)
    serializer = ReviewSerializer(
        instance=review, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@review_exists
@review_write_permission
def delete_review(request, pk):
    review = Review.objects.get(id=pk)
    review.delete()
    return Response("Review deleted", status=status.HTTP_200_OK)

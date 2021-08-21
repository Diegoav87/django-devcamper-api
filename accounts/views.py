from django.shortcuts import render

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .serializers import CustomUserSerializer


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        if user:
            return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

from .serializers import CustomUserSerializer, GetUserSerializer, UserEditSerializer, UpdatePasswordSerializer
from accounts.models import CustomUser


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        if user:
            return Response(status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    serializer = GetUserSerializer(user)
    return Response({"user": serializer.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_user(request):
    serializer = UserEditSerializer(
        instance=request.user, data=request.data, partial=True, context={"request": request})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UpdatePasswordSerializer

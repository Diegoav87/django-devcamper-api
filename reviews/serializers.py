from rest_framework import serializers

from .models import Review
from bootcamps.serializers import BootcampSimpleSerializer
from accounts.serializers import GetUserSerializer


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('text', 'rating', 'title')

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                "The rating has to be a number between 1 and 10")
        return value


class ReviewGetSerializer(serializers.ModelSerializer):
    bootcamp = BootcampSimpleSerializer(read_only=True)
    user = GetUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"

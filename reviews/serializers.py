from rest_framework import serializers

from .models import Review
from bootcamps.serializers import BootcampListSerializer


class ReviewSerializer(serializers.ModelSerializer):
    bootcamp = BootcampListSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'rating', 'bootcamp')

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                "The rating has to be a number between 1 and 10")
        return value

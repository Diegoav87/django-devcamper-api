from django.db import models

from bootcamps.models import Bootcamp
from accounts.models import CustomUser

# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="reviews", on_delete=models.CASCADE)
    bootcamp = models.ForeignKey(
        Bootcamp, related_name="reviews", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    text = models.TextField(max_length=500)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username}: {self.rating}"

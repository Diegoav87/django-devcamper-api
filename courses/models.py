from django.db import models
from django.db.models.fields import related

from bootcamps.models import Bootcamp

# Create your models here.


class Course(models.Model):
    SKILL = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    bootcamp = models.ForeignKey(
        Bootcamp, on_delete=models.CASCADE, related_name="courses")
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    weeks = models.CharField(max_length=255)
    tuition = models.IntegerField()
    minimum_skill = models.CharField(max_length=255, choices=SKILL)
    scolarship_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

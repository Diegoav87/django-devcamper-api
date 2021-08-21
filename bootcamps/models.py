from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator, FileExtensionValidator

from accounts.models import CustomUser
# Create your models here.


class Career(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Bootcamp(models.Model):
    user = models.ForeignKey(CustomUser, related_name="bootcamps",
                             on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(validators=[RegexValidator(
        '^\+?1?\d{9,15}$', message="The phone number should be in format: '+999999999'. Up to 15 digits allowed")], blank=True, null=True, max_length=20)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.CharField(max_length=255)
    careers = models.ManyToManyField(Career, blank=True)
    average_rating = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)], blank=True, null=True)
    photo = models.ImageField(upload_to="images/", blank=True, null=True, validators=[
                              FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
    # average_cost
    housing = models.BooleanField(default=False)
    job_assistance = models.BooleanField(default=False)
    job_guarantee = models.BooleanField(default=False)
    accept_gi = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_average_cost(self):
        average = 0

        for course in self.courses.all():
            average += course.tution

        average = average / self.courses.count()
        return average

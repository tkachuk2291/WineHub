import re
from django.db import models
from pathlib import Path

from rest_framework.exceptions import ValidationError


def starts_with_letter_validator(value):
    if not re.match(r'^[a-zA-Z]', value):
        raise ValidationError('The value must start with a letter.')


class Winery(models.Model):
    name = models.CharField(
        max_length=10, unique=True, validators=[starts_with_letter_validator])

    def __str__(self):
        return self.name


class WineType(models.Model):
    type = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.type} wine"


class Location(models.Model):
    country = models.CharField(max_length=20, validators=[starts_with_letter_validator])
    region = models.CharField(max_length=50, validators=[starts_with_letter_validator])

    def __str__(self):
        return f"Country: {self.country}, Region: {self.region}"


class Rating(models.Model):
    average = models.DecimalField(max_digits=3, decimal_places=2)
    reviews = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.average} ({self.reviews} reviews)"


class Preferences(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    wine_type = instance.wine_type.type

    path = Path(f"upload/wine/{wine_type}/{filename}")
    return path


class Wine(models.Model):
    wine_type = models.ForeignKey(WineType, on_delete=models.CASCADE)
    winery = models.ForeignKey(Winery, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, validators=[starts_with_letter_validator])
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    image_upload = models.ImageField(upload_to=upload_to, null=True, blank=True)
    image_url = models.URLField(null=True)
    vintage = models.PositiveIntegerField(max_length=4, null=True)
    price = models.IntegerField()
    preferences = models.ManyToManyField(Preferences, related_name='wine_preferences')

    def __str__(self):
        return f"{self.name} ({self.vintage})"

    def save(self, *args, **kwargs):
        if not self.image_upload:
            self.image_upload = None
        super().save(*args, **kwargs)

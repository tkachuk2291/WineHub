from django.core.validators import MaxLengthValidator
from django.db import models
from pathlib import Path


class Winery(models.Model):
    name = models.CharField(
        max_length=140, unique=True,
        validators=[MaxLengthValidator(limit_value=100, message=f"name for wine is too long max 100")])

    def __str__(self):
        return self.name


class WineType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.type} wine"


class Location(models.Model):
    country = models.CharField(max_length=255)
    region = models.CharField(max_length=256)

    def __str__(self):
        return f"Country: {self.country}, Region: {self.region}"


class Rating(models.Model):
    average = models.DecimalField(max_digits=3, decimal_places=2)
    reviews = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.average} ({self.reviews} reviews)"


def upload_to(instance, filename):
    wine_type = instance.wine_type.type

    path = Path(f"upload/wine/{wine_type}/{filename}")
    return path


class Wine(models.Model):
    wine_type = models.ForeignKey(WineType, on_delete=models.CASCADE)
    winery = models.ForeignKey(Winery, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    image_upload = models.ImageField(upload_to=upload_to, null=True, blank=True)
    image_url = models.URLField(null=True)
    vintage = models.PositiveIntegerField(max_length=4, null=True)

    def __str__(self):
        return f"{self.name} ({self.vintage})"

    def save(self, *args, **kwargs):
        if not self.image_upload:
            self.image_upload = None
        super().save(*args, **kwargs)

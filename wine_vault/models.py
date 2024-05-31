from django.db import models


class Winery(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Location(models.Model):
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.country} · {self.region}"


class Rating(models.Model):
    average = models.DecimalField(max_digits=3, decimal_places=2)
    reviews = models.PositiveIntegerField()
    wine = models.ForeignKey("Wine", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.average} ({self.reviews} reviews)"


class Wine(models.Model):
    name = models.CharField(max_length=255)
    vintage = models.PositiveIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"{self.name} ({self.vintage})"


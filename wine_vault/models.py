from django.db import models


class Winery(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WineType(models.Model):
    type = models.CharField(max_length=255)


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


class Wine(models.Model):
    wine_type = models.ForeignKey(WineType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    image_url = models.URLField()
    vintage = models.PositiveIntegerField(max_length=4, null=True)

    def __str__(self):
        return f"{self.name} ({self.vintage})"

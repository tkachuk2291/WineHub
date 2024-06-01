from rest_framework import serializers

from wine_vault.models import Wine, Rating, Location, WineType


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("average", "reviews")


class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("country", "region")


class WineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineType
        fields = ("type",)


class AllWinesSerializer(serializers.ModelSerializer):
    rating = RatingSerializer()
    location = LocationSerializers()
    wine_type = WineTypeSerializer()

    class Meta:
        model = Wine
        fields = ("name", "vintage", "location", "rating", "image_url", "wine_type")

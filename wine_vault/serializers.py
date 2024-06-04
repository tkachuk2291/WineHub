from rest_framework import serializers

from wine_vault.models import Wine, Rating, Location, WineType, Winery


class WinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Winery
        fields = 'name'


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


class WinesSerializer(serializers.ModelSerializer):
    rating = RatingSerializer()
    location = LocationSerializers()
    wine_type = WineTypeSerializer()

    class Meta:
        model = Wine
        fields = ("name", "vintage", "winery", "location", "rating", "image_url", "wine_type", "image_upload")


class WineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = ("name", "vintage", "location", "rating", "winery", "image_url", "wine_type", "image_upload")

    def create(self, validated_data):
        return Wine.objects.create(**validated_data)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = ("image_upload", "image_url")

from rest_framework import serializers

from wine_vault.models import Wine, Rating, Location, WineType, Winery, Preferences


class PreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
        fields = ('id', 'name')


class WinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Winery
        fields = ('id', 'name')


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
        fields = ("id", "type",)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "country", "region")


class WineFavoriteBottleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = ("id", "name")


class WinesSerializer(serializers.ModelSerializer):
    rating = RatingSerializer()
    location = LocationSerializers()
    wine_type = WineTypeSerializer()
    preferences = PreferencesSerializer(many=True)
    winery = WinerySerializer()

    class Meta:
        model = Wine
        fields = ("name", "vintage", "winery", "location", "rating", "image_url", "wine_type", "image_upload", "price",
                  "preferences")


class WineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = (
            "name", "vintage", "location", "rating", "winery", "image_url", "wine_type", "image_upload", "preferences")

    def create(self, validated_data):
        return Wine.objects.create(**validated_data)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wine
        fields = ("image_upload", "image_url")

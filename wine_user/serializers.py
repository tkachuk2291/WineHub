from rest_framework import serializers

from wine_user.models import WineUser, UserFavoriteBottle
from wine_vault.serializers import WinerySerializer


class UserWineSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineUser
        fields = ('id', 'username', "first_name", "last_name")


class UserFavoriteBottleSerializer(serializers.ModelSerializer):
    wine = WinerySerializer
    user = UserWineSerializer

    class Meta:
        model = UserFavoriteBottle
        fields = ("id", "user", "wine")

from django.contrib.auth import get_user_model

from wine_user.models import WineUser, UserFavoriteBottle
from wine_user.validators import password_validate
from wine_vault.serializers import WinerySerializer

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ('email', 'password')


class UserWineSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = WineUser(
            email=validated_data['email'],
            age=validated_data['age'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, value):
        password_validate(value)
        return value

    class Meta:
        model = WineUser
        fields = ('id', 'email', "first_name", "last_name", "age", "password")


class UserFavoriteBottleSerializer(serializers.ModelSerializer):
    wine = WinerySerializer
    user = UserWineSerializer

    class Meta:
        model = UserFavoriteBottle
        fields = ("id", "user", "wine")

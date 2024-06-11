from rest_framework import viewsets

from wine_user.models import WineUser, UserFavoriteBottle
from wine_user.serializers import UserWineSerializer, UserFavoriteBottleSerializer


class UserWineViewSet(viewsets.ModelViewSet):
    queryset = WineUser.objects.all()
    model = WineUser
    serializer_class = UserWineSerializer


class UserFavoriteBottleViewSet(viewsets.ModelViewSet):
    model = UserFavoriteBottle
    queryset = UserFavoriteBottle.objects.all()
    serializer_class = UserFavoriteBottleSerializer



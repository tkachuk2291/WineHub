from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.response import Response

from wine_user.models import WineUser, UserFavoriteBottle
from wine_user.serializers import UserWineSerializer, UserFavoriteBottleSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from wine_user.serializers import TokenObtainPairSerializer


class UserWineViewSet(viewsets.ModelViewSet):
    queryset = WineUser.objects.all()
    model = WineUser
    serializer_class = UserWineSerializer


class UserFavoriteBottleViewSet(viewsets.ModelViewSet):
    model = UserFavoriteBottle
    queryset = UserFavoriteBottle.objects.all()
    serializer_class = UserFavoriteBottleSerializer
    def get_queryset(self):
        user = self.request.user
        return UserFavoriteBottle.objects.filter(user=user)


class RegisterView(APIView):
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        serializer = UserWineSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

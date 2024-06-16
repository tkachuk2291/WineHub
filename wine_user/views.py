from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from wine_user.models import WineUser, UserFavoriteBottle
from wine_user.serializers import UserWineSerializer, UserFavoriteBottleSerializer, UserFavoriteBottleAddSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from wine_user.serializers import TokenObtainPairSerializer


class UserWineViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = WineUser.objects.all()
    model = WineUser
    serializer_class = UserWineSerializer


class UserFavoriteBottleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    model = UserFavoriteBottle
    queryset = UserFavoriteBottle.objects.all()
    serializer_class = UserFavoriteBottleSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavoriteBottleSerializer
        elif self.action == "retrieve":
            return UserFavoriteBottleAddSerializer
        elif self.action == "create":
            return UserFavoriteBottleAddSerializer
        return UserFavoriteBottleSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return UserFavoriteBottle.objects.filter(user=user)


class RegisterView(APIView):
    serializer_class = UserWineSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserWineSerializer(data=request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return JsonResponse({"message": "Account created successfully"}, status=HTTP_201_CREATED)
        return JsonResponse({"errors": serializer.errors}, status=HTTP_400_BAD_REQUEST)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

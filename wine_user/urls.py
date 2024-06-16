from rest_framework.routers import DefaultRouter

from wine_user.views import UserWineViewSet, UserFavoriteBottleViewSet, RegisterView
from django.urls import path, include

router = DefaultRouter()

router.register("user", UserWineViewSet, basename="user"),
router.register("user-favorite-bottle", UserFavoriteBottleViewSet, basename="user-favorite-bottle"),

urlpatterns = [path("", include(router.urls)),
               path("register/", RegisterView.as_view())]

app_name = "wine_user"

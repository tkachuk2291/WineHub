from django.urls import path, include
from rest_framework.routers import DefaultRouter

from wine_vault.views import AllWinesViewSet, RedWineViewSet, PortWineViewSet, DessertWineViewSet, RoseWineViewSet, \
    SparklingWineViewSet, WhiteWineViewSet, PickRandomBottleWine

router = DefaultRouter()

router.register("all", AllWinesViewSet, basename="all-wines")
router.register("reds", RedWineViewSet, basename="red-wines")
router.register("whites", WhiteWineViewSet, basename="whites-wines")
router.register("sparkling", SparklingWineViewSet, basename="sparkling-wines")
router.register("rose", RoseWineViewSet, basename="rose-wines")
router.register("dessert", DessertWineViewSet, basename="dessert-wines")
router.register("port", PortWineViewSet, basename="port-wines")

urlpatterns = [path("", include(router.urls)),
               path("random-bottle-wine/", PickRandomBottleWine.as_view(), name="random-bottle")]
app_name = "wine_vault"

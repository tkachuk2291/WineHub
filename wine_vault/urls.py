from django.urls import path, include
from rest_framework.routers import DefaultRouter

from wine_vault.views import AllWinesViewSet, RedWineViewSet, PortWineViewSet, DessertWineViewSet, RoseWineViewSet, \
    SparklingWineViewSet, WhiteWineViewSet, PickRandomBottleWine, BestSellers, WineryModelViewSet, WineTypeModelViewSet, \
    LocationModelViewSet, RatingModelViewSet

router = DefaultRouter()

router.register("all", AllWinesViewSet, basename="all-wines")
router.register("reds", RedWineViewSet, basename="red-wines")
router.register("whites", WhiteWineViewSet, basename="whites-wines")
router.register("sparkling", SparklingWineViewSet, basename="sparkling-wines")
router.register("rose", RoseWineViewSet, basename="rose-wines")
router.register("dessert", DessertWineViewSet, basename="dessert-wines")
router.register("port", PortWineViewSet, basename="port-wines")
router.register("winery", WineryModelViewSet, basename="winery-wines"),
router.register("wine-type", WineTypeModelViewSet, basename="wine-type"),
router.register("location", LocationModelViewSet, basename="location"),
router.register("rating", RatingModelViewSet, basename="rating"),

urlpatterns = [path("", include(router.urls)),
               path("random-bottle-wine/", PickRandomBottleWine.as_view(), name="random-bottle"),
               path("bestsellers-three-bottle-wine", BestSellers.as_view(), name="bestSellers-three-bottle"),
               ]
app_name = "wine_vault"

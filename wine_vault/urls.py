from django.urls import path, include
from rest_framework.routers import DefaultRouter

from wine_vault.views import AllWinesViewSet

router = DefaultRouter()

router.register("all", AllWinesViewSet , basename="all-wines")
# router.register("reds",  , basename="red-wines")
# router.register("whites",  , basename="red-wines")
# router.register("sparkling",  , basename="sparkling-wines")
# router.register("rose",  , basename="rose-wines")
# router.register("dessert",  , basename="dessert-wines")
# router.register("port",  , basename="port-wines")







urlpatterns = [path("", include(router.urls))]
app_name = "wine_vault"

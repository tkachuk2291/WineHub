from rest_framework import viewsets

from wine_vault.models import Wine
from wine_vault.serializers import WinesSerializer


class AllWinesViewSet(viewsets.ModelViewSet):
    queryset = Wine.objects.all()
    model = Wine
    serializer_class = WinesSerializer


class RedWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        queryset = Wine.objects.all().filter(wine_type__type="red")



class WhiteWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return Wine.objects.all().filter(wine_type__type="white")


class SparklingWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return Wine.objects.all().filter(wine_type__type="sparkling")


class RoseWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return Wine.objects.all().filter(wine_type__type="rose")


class DessertWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return Wine.objects.all().filter(wine_type__type="dessert")


class PortWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return Wine.objects.all().filter(wine_type__type="port")

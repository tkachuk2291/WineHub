from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from wine_vault.models import Wine
from wine_vault.serializers import WinesSerializer, ImageSerializer


def filtering_query(type_wine_filtering, params):
    queryset = Wine.objects.filter(wine_type__type=type_wine_filtering)
    name = params.request.query_params.get("name")
    country = params.request.query_params.get("country")
    region = params.request.query_params.get("region")
    average = params.request.query_params.get("average")
    reviews = params.request.query_params.get("reviews")
    vintage = params.request.query_params.get("vintage")

    if name:
        queryset = queryset.filter(
            name__icontains=name
        )
    if country:
        queryset = queryset.filter(
            location__country__icontains=country
        )
    if region:
        queryset = queryset.filter(
            location__region__icontains=region
        )

    if average:
        queryset = queryset.filter(
            rating__average__icontains=average
        )
    if reviews:
        queryset = queryset.filter(
            rating__reviews__icontains=reviews
        )
    if vintage:
        queryset = queryset.filter(
            vintage=vintage
        )

    return queryset.distinct()


class RedWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return filtering_query(type_wine_filtering="red", params=self)

    def get_serializer_class(self):
        if self.action == "list":
            return WinesSerializer
        elif self.action == "upload_image":
            return ImageSerializer
        return WinesSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request):
        wine_hub = self.get_object()
        serializer = self.get_serializer(wine_hub, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WhiteWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return filtering_query(type_wine_filtering="white", params=self)


class SparklingWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return filtering_query(type_wine_filtering="sparkling", params=self)


class RoseWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return filtering_query(type_wine_filtering="rose", params=self)


class DessertWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return filtering_query(type_wine_filtering="dessert", params=self)


class PortWineViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer

    def get_queryset(self):
        return filtering_query(type_wine_filtering="port", params=self)


class AllWinesViewSet(viewsets.ModelViewSet):
    model = Wine
    serializer_class = WinesSerializer
    Wine.objects.all()

    def get_queryset(self):
        queryset = Wine.objects.all()
        name = self.request.query_params.get("name")
        country = self.request.query_params.get("country")
        region = self.request.query_params.get("region")
        average = self.request.query_params.get("average")
        reviews = self.request.query_params.get("reviews")
        vintage = self.request.query_params.get("vintage")
        wine_type = self.request.query_params.get("wine_type")

        if name:
            queryset = queryset.filter(
                name__icontains=name
            )
        if country:
            queryset = queryset.filter(
                location__country__icontains=country
            )
        if region:
            queryset = queryset.filter(
                location__region__icontains=region
            )

        if average:
            queryset = queryset.filter(
                rating__average__icontains=average
            )
        if reviews:
            queryset = queryset.filter(
                rating__reviews__icontains=reviews
            )
        if vintage:
            queryset = queryset.filter(
                vintage=vintage
            )
        if wine_type:
            queryset = queryset.filter(
                wine_type__type__icontains=wine_type
            )

        return queryset.distinct()

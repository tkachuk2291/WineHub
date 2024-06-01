from django.shortcuts import render
from rest_framework import serializers, viewsets

from wine_vault.models import Wine
from wine_vault.serializers import AllWinesSerializer


class AllWinesViewSet(viewsets.ModelViewSet):
    queryset = Wine.objects.all()
    model = Wine
    serializer_class = AllWinesSerializer

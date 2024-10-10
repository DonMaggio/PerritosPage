from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import PerroSerizalizer
from .models import Perro

# Create your views here.
def index(request):
    return HttpResponse("Index")

class PerritosViewSet(viewsets.ModelViewSet):
    queryset = Perro.objects.all().filter(status=True)
    serializer_class = PerroSerizalizer
    permission_classes = [IsAuthenticatedOrReadOnly]
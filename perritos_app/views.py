from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer

from .serializers import PerroSerizalizer
from .models import Perro

from .permissions import IsAdminOrReadOnly

# Create your views here.
def index(request):
    return render(request, 'index.html')

class PerritosViewSet(viewsets.ModelViewSet):
    serializer_class = PerroSerizalizer
    permission_classes = [IsAdminOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer, BrowsableAPIRenderer, JSONRenderer]

    def get_queryset(self):
        return Perro.objects.all().filter(status=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.accepted_renderer.format == 'html':
            return Response({'perros': queryset}, template_name='perritos_list.html')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Forzar respuesta en JSON si se pasa un parámetro en la URL ?format=json
        if request.accepted_renderer.format == 'html':
            return Response({'perro': instance}, template_name='perrito_detail.html')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from .serializers import PerroSerizalizer
from .models import Perro

from .permissions import IsAdminOrReadOnly

# Create your views here.
def index(request):
    return HttpResponse("Index")

class PerritosViewSet(viewsets.ModelViewSet):
    serializer_class = PerroSerizalizer
    permission_classes = [IsAdminOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name='perritos_lista.html'

    def get_queryset(self):
        return Perro.objects.all().filter(status=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.accepted_renderer.format == 'html':
            return Response({'perros': queryset}, template_name=self.template_name)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.accepted_renderer.format == 'html':
            return Response({'perro': instance}, template_name='detalle_perro.html')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
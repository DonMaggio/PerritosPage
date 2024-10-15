from django.forms import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer

from .serializers import PerroSerizalizer
from .models import Perro, PerroFotos
from .forms import PerrosForm, PerroFotosForm

from .permissions import IsAdminOrReadOnly

# Create your views here.
def index(request):
    return render(request, 'index.html')

# View para listar todas las entradas o solo de a una
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


#Form para cargar una nueva instancia
class PerritosFormView(FormView):
    form_class = PerrosForm
    template_name = 'perrito_create.html'
    success_url = reverse_lazy('adopta-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imageform'] = PerroFotosForm()
        return context

    def form_valid(self, form):
        files = self.request.FILES.getlist('file_field')
        perro = form.save(commit = False)
        perro.user = self.request.user
        perro.save()

        for f in files:
            PerroFotos.objects.create(perro=perro, imagen=f)
        messages.success(self.request, "Nuevo perro agregado")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))


#View para editar las entradas
class PerritosUpdateView(UpdateView):
    model = Perro
    form_class = PerrosForm
    template_name = 'perrito_update.html'
    success_url = reverse_lazy('adopta-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imageform'] = PerroFotosForm()
        context['perro_fotos'] = PerroFotos.objects.filter(perro=self.object)
        return context
    
    def form_valid(self, form):
        perro = form.save(commit=False)
        perro.save()
        PerroFotos.objects.filter(perro=perro).delete()
        files = self.request.FILES.getlist('file_field')
        for f in files:
            PerroFotos.objects.create(perro=perro, imagen=f)

        messages.success(self.request, 'Información del perro actualizada')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
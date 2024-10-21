from django.forms import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from drf_spectacular.utils import extend_schema

from .serializers import PerroListSerizalizer, PerroDetailSerizalizer
from .models import Perro, PerroFotos
from .forms import PerrosForm, PerroFotosForm

from .permissions import IsAdminOrReadOnly

# Create your views here.
class IndexView(TemplateView):
    template_name='index.html'

class TransitaView(TemplateView):
    template_name='transita.html'

class DonaView(TemplateView):
    template_name='dona.html'

# View para listar todas las entradas o solo de a una
class PerritosViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Perro.objects.all().filter(status=True).order_by('id')
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name='perritos_list.html'

    def get_serializer_class(self):
        if self.action == 'list':
            return PerroListSerizalizer
        if self.action == 'retrieve':
            return PerroDetailSerizalizer
        return super().get_serializer_class()

    def render_response(self, data, request, template_name=None, context=None):
        """Función para manejar la respuesta HTML o JSON."""
        context = context or {}
        if request.accepted_renderer.format == 'html':
            return Response({**context, 'perros': data}, template_name=template_name)
        return Response(data)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page or queryset, many=True).data
        
        if page is not None:
            paginated_response = self.get_paginated_response(data)
            pagination_data = {
                'total_pages': paginated_response.data.get('count') // self.paginator.page_size + 1,
                'current_page': self.paginator.page.number,
                'has_next': self.paginator.page.has_next(),
                'has_previous': self.paginator.page.has_previous(),
            }
            return self.render_response(data, request, template_name=self.template_name, context=pagination_data)
        
        return self.render_response(data, request, template_name=self.template_name)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        return self.render_response(data, request, template_name='perrito_detail.html')


#View con form para cargar una nueva instancia
class PerritosFormView(LoginRequiredMixin, FormView):
    form_class = PerrosForm
    template_name = 'perrito_create.html'
    success_url = reverse_lazy('adopta-list')
    #login_url = "/login/"
    #redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imageform'] = PerroFotosForm()
        return context

    def form_valid(self, form):
        files = self.request.FILES.getlist('file_field')
        if not files:
            form.add_error(None, 'Debe subir al menos una imagen.')
            return self.form_invalid(form)
        
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


#View con form para editar las entradas
class PerritosUpdateView(LoginRequiredMixin, UpdateView):
    model = Perro
    form_class = PerrosForm
    template_name = 'perrito_update.html'
    success_url = reverse_lazy('adopta-list')
    #login_url = "/login/"
    #redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imageform'] = PerroFotosForm()
        context['perro_fotos'] = PerroFotos.objects.filter(perro=self.object)
        return context
    
    def form_valid(self, form):
        perro = form.save(commit=False)
        perro.save()
        files = self.request.FILES.getlist('file_field')
        if not files:
            form.add_error(None, 'Debe subir al menos una imagen.')
            return self.form_invalid(form)

        PerroFotos.objects.filter(perro=perro).delete()
        for f in files:
            PerroFotos.objects.create(perro=perro, imagen=f)

        messages.success(self.request, 'Información del perro actualizada')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
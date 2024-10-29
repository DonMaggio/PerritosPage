from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView, UpdateView
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer
from drf_spectacular.utils import extend_schema

import json

from .serializers import PerroListSerizalizer, PerroDetailSerizalizer
from .models import Perro, PerroFotos
from .forms import PerrosForm, PerroFotosForm, RegisterUserForm

from .permissions import IsAdminOrReadOnly

# Create your views here.
class IndexView(generic.TemplateView):
    template_name='index.html'

class TransitaView(generic.TemplateView):
    template_name='transita.html'

class DonaView(generic.TemplateView):
    template_name='dona.html'


class PerritosListView(generic.ListView):
    permission_classes = [IsAdminOrReadOnly]
    model = Perro
    template_name = 'perritos_list.html'
    context_object_name = 'perros'
    paginate_by = 12  # Si deseas paginar la lista

    def get_queryset(self):
        return Perro.objects.filter(status=True).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username if self.request.user.is_authenticated else 'Anónimo'
        return context
    

class PerritoDetailView(generic.DetailView):
    permission_classes = [IsAdminOrReadOnly]
    model = Perro
    template_name = 'perrito_detail.html'
    context_object_name = 'perro'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username if self.request.user.is_authenticated else 'Anónimo'
        return context

#View con form para cargar una nueva instancia
class PerritosFormView(LoginRequiredMixin, FormView):
    form_class = PerrosForm
    template_name = 'perrito_create.html'
    success_url = reverse_lazy('adopta-list')
    login_url = "index"
    redirect_field_name = "redirect_to"

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
    login_url = "index"
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imageform'] = PerroFotosForm()
        context['perro_fotos'] = PerroFotos.objects.filter(perro=self.object)
        return context
    
    def form_valid(self, form):
        perro = form.save(commit=False)
        perro.save()

        # Capturar los IDs de las imágenes que se seleccionaron para eliminar
        delete_ids = self.request.POST.get('delete_fotos')
        if delete_ids:
            delete_ids = json.loads(delete_ids)  # Convertir de JSON a lista de IDs
            #PerroFotos.objects.filter(id__in=delete_ids, perro=perro).delete()
            for foto_id in delete_ids:
                foto = PerroFotos.objects.get(id=foto_id)
                foto.delete()  # Esto invocará el método delete del modelo y eliminará la imagen del disco

        # Procesar los archivos nuevos si existen
        files = self.request.FILES.getlist('file_field')
        if files:
            # Si hay nuevos archivos, agregar las nuevas fotos
            for f in files:
                PerroFotos.objects.create(perro=perro, imagen=f)
        
        else:
            # Validar que al menos haya una imagen asociada al perro
            if not PerroFotos.objects.filter(perro=perro).exists():
                form.add_error(None, 'Debe mantener al menos una imagen.')
                return self.form_invalid(form)

        messages.success(self.request, 'Información del perro actualizada')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

## Gestion de usuarios
class RegisterView(View):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, self.template_name, {'form':form})
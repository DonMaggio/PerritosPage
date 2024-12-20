from django.urls import path, include

from rest_framework.routers import DefaultRouter

#Documentacion Swagger
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views
from .views import PerritosFormView, PerritosUpdateView, IndexView, TransitaView, DonaView, RegisterView
from .views import PerritosListView, PerritoDetailView

#router = DefaultRouter()
#router.register(r'perro', PerritosViewSet, basename='adopta')

urlpatterns = [
    #path('', include(router.urls)),

    #Documentacion
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('perro/', PerritosListView.as_view(), name='adopta-list'),
    path('perro/<int:pk>/', PerritoDetailView.as_view(), name='adopta-detail'),
    path('nosotros/', IndexView.as_view(), name='index'),
    path('transita/', TransitaView.as_view(), name='transita'),
    path('dona/', DonaView.as_view(), name='dona'),
    path('perro/create/', PerritosFormView.as_view(), name='perro-create'),
    path('perro/update/<int:pk>', PerritosUpdateView.as_view(), name='perro-update'),

    #Gestion de usuarios
    path('account/register', RegisterView.as_view(), name='register'),

]
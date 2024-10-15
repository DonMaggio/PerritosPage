from django.urls import path, include

from rest_framework.routers import DefaultRouter

#Documentacion Swagger
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views
from .views import PerritosViewSet, PerritosFormView, PerritosUpdateView

router = DefaultRouter()
router.register(r'perritos', PerritosViewSet, basename='adopta')

urlpatterns = [
    path('', include(router.urls)),

    #Documentacion
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('', views.index, name='index'),
    path('perro/create', PerritosFormView.as_view(), name='perro-create'),
    path('perro/update/<int:pk>', PerritosUpdateView.as_view(), name='perro-update'),
]
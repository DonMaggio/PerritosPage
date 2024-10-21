from django.urls import path, include

from rest_framework.routers import DefaultRouter

#Documentacion Swagger
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views
from .views import PerritosViewSet, PerritosFormView, PerritosUpdateView, IndexView, TransitaView, DonaView

router = DefaultRouter()
router.register(r'perro', PerritosViewSet, basename='adopta')

urlpatterns = [
    path('', include(router.urls)),

    #Documentacion
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('nosotros', IndexView.as_view(), name='index'),
    path('transita', TransitaView.as_view(), name='transita'),
    path('dona', DonaView.as_view(), name='dona'),
    path('perro/create', PerritosFormView.as_view(), name='perro-create'),
    path('perro/update/<int:pk>', PerritosUpdateView.as_view(), name='perro-update'),
]
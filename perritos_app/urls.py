from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views
from .views import PerritosViewSet

router = DefaultRouter()
router.register(r'perritos', PerritosViewSet, basename='adopta')

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),
]

from django.urls import include, path, re_path
from rest_framework import routers

from . import admin, views
from .views import *

app_name = 'real_turismo'
router = routers.DefaultRouter()
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'veiculos', VeiculoViewSet)
router.register(r'postos', PostoViewSet)
router.register(r'abastecimentos', AbastecimentoViewSet)
router.register(r'auth', views.AuthViewSet, basename='auth')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

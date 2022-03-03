from rest_framework import routers
from seguridad.viewsets import *
from django.urls import path
from knox import views as knox_views
"""
 APIS Gym
"""
neymatex_api = routers.DefaultRouter()
neymatex_api.register(r'usuarios', DetallesView, 'usuario')
"""
 APIS Seguridad
"""
seguridad_api = [path('registrarse/', RegistrarAPI.as_view(), name='regitrarse'),
                 path('login/', LoginAPI.as_view(), name='login'),
                 path('logout/', knox_views.LogoutView.as_view(), name='logout'),
                 path('logoutall/', knox_views.LogoutAllView.as_view(),
                      name='logoutall'),
                 path("validate/", TokenValidatorAPI.as_view(),
                      name="validate_token")
                 ]

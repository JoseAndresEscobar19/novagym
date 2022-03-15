from django.urls import path
from knox import views as knox_views
from membresia.viewsets import (BeneficioViewSet, DescuentoViewSet,
                                MembresiaViewSet)
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet
from rest_framework import routers
from seguridad.viewsets import (DetallesViewSet, LoginAPI, RegistrarAPI,
                                TokenValidatorAPI)

"""
 APIS Gym
"""
novagym = routers.DefaultRouter()
novagym.register('usuarios', DetallesViewSet, 'usuario')
novagym.register('membresias', MembresiaViewSet, 'membresia')
novagym.register('descuentos', DescuentoViewSet, 'descuento')
novagym.register('beneficios', BeneficioViewSet, 'beneficio')
novagym.register(r'registrar/gcm', GCMDeviceAuthorizedViewSet)
novagym_api = novagym.urls

"""
 APIS Seguridad
"""
seguridad_api = [
    path('registrarse/', RegistrarAPI.as_view(), name='regitrarse'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(),
         name='logoutall'),
    path("validate/", TokenValidatorAPI.as_view(),
         name="validate_token")
]

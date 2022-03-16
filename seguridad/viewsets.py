from django.contrib.auth import login
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

# API


class RegistrarAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrarSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def get_post_response_data(self, request, token, instance):
        data = super().get_post_response_data(request, token, instance)
        try:
            usuario = UserDetails.objects.get(usuario=request.user)
            usuario_serializer = DetalleSerializer(usuario).data
            data['user']['detalles'] = usuario_serializer
        except UserDetails.DoesNotExist:
            print("No existe el usuario.")
        return data

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_active:
            return Response({
                "detail": 'Usuario deshabilitado. Contácte Administración'
            }, status=status.HTTP_423_LOCKED)
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class DetallesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UsuarioDetallesSerializer
    queryset = UserDetails.objects.all()
    http_method_names = ['get', 'put', 'patch' ,'head']

class TokenValidatorAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({
            "detail": request.user.is_authenticated
        })

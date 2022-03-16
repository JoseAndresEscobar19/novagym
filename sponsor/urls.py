from django.urls import path
from .views import *
from .apps import SponsorConfig

app_name = SponsorConfig.name


urlpatterns = [
     path('listar/', ListarSponsors.as_view(), name='listar'),
     #path('create/', createSponsor, name='createSponsor'),
     path('sponsor-list/', sponsorList, name='sponsor-overview'),
     path('sponsor-detail/<str:id>', sponsorDetail, name='sponsor-detail'),
     path('sponsor-create/', sponsorCreate, name='sponsor-create'),
     path('sponsor-update/<str:id>', sponsorUpdate, name='sponsor-update'),
     path('sponsor-delete/<str:id>', sponsorDelete, name='sponsor-delete'),
     path('eliminar/<int:id>/', deleteSponsor, name='eliminar'),
     path('crear/', CrearSponsor.as_view(), name='crear'),
     path('editar/<str:pk>', UpdateSponsor.as_view(), name='update'),
     path('change/<str:pk>', ChangeState, name='change'),
     path('getSponsors/', getAllSponsors, name='getSponsors'),
]
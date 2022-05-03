from django.urls import path
from calendario.views import *
from .apps import CalendarioConfig

app_name = CalendarioConfig.name


urlpatterns = [
    path('listarZona',ShowZona.as_view(),name="listarZona"),
    path('crearZona/',CrearZona.as_view(),name="crearZona"),
    path('listar',ShowCalendario.as_view(),name="listar"),
    path('crear/',CrearCalendario.as_view(),name="crear"),
    path('editar/<int:pk>',UpdateCalendario.as_view(),name="editar"),
    path('eliminar/<int:id>',deleteCalendario,name="eliminar"),
    path('getHorarios/',getHorarios,name="getHorarios"),
    path('verClases/',Horarios.as_view(),name="verClases"),
    path('verClases/<int:opcion>',Horarios.as_view(),name="verClases"),
    path('verReservas/',HorariosReservas.as_view(),name="verReservas"),
    path('verReservas/<int:opcion>',HorariosReservas.as_view(),name="verReservas"),
    path('updateZona/<int:pk>',UpdateZona.as_view(),name="updateZona"),
    path('eliminarZona/<int:id>',deleteZona,name="eliminarZona"),

    path('datosHorario/',HorarioSmall.as_view(),name="datosHorario"),
    path('datosHorario/<int:opc>',HorarioSmall.as_view(),name="datosHorario"),

    path('reservarClase/',Reservar.as_view(),name="reservarClase"),
    path('reservarMaquina/',ReservarMaquina.as_view(),name="reservarMaquina"),    
    path('maquinasDispo/',MaquinasDispo.as_view(),name="maquinasDispo"),
    path('horariosDispo/',HorariosDispo.as_view(),name="horariosDispo"),
    path('horariosUsuario/<int:id>',HorariosUsuario.as_view(),name="horariosUsuario"),
    path('maquinasUsuario/<int:id>',MaquinaUsuario.as_view(),name="maquinasUsuario"),
    path('verificarMaquina/',VerificarMaquina.as_view(),name="verificarMaquina"),
]
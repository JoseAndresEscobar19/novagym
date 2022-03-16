from django.urls import path
from .views import *
from .apps import ContactenosConfig

app_name = ContactenosConfig.name

urlpatterns = [
     #Gimnasio-Contacto
     
    path('', contact, name='contact'),
    path('sendEmail/', sendEmail, name='sendEmail'),
    path('SendMail/', SendMail.as_view(), name='SendMail'),
    path('buzon/', ShowBuzon.as_view(), name='buzon'),
    path('buzon/leidos', ShowBuzonLeidos.as_view(), name='buzonLeidos'),
    path('buzon/noLeidos', ShowBuzonNoLeidos.as_view(), name='buzonNoLeidos'),
    path('markAsRead/<int:id>', markAsRead, name='markAsRead'),
    path('eliminar/<int:id>', deleteMail, name='eliminar'),
    path('leer/<int:id>', readMail, name='leer')
]
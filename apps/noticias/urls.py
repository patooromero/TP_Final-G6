from django.urls import path
from . import views

app_name = 'noticias'

urlpatterns = [
    path('', views.Listar_Noticias, name='listar'),
    path('Detalle/<int:pk>', views.Detalle_Noticias, name='detalle'),
    path('Comentario/', views.Comentar_Noticia, name='comentar'),
    path('Comentario/Eliminar/<int:pk>', views.Eliminar_Comentario, name='eliminar_comentario'),
    path('Crear/', views.Crear_Noticia, name='crear'),
]


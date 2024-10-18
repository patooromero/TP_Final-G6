
from django.urls import path, include
from . import views
from .views import bloquear_usuario

app_name = 'noticias'

urlpatterns = [
	
	path('', views.Listar_Noticias, name = 'listar'),

	path('Detalle/<int:pk>', views.Detalle_Noticias, name = 'detalle'),
	
	path('Comentario/', views.Comentar_Noticia, name = 'comentar'),
    
    path('crear/', views.Crear_Noticia, name='crear_noticia'),
    
	path('categoria/crear/', views.Crear_Categoria, name='crear_categoria'),
    
    path('comentario/delete/<int:comment_id>', views.delete_comment, name='delete_comment'),
    
	path('noticias/eliminar/<pk>/', views.eliminar_noticia, name='eliminar_noticia'),
    
	path('perfil/<pk>/', views.perfil_usuario, name='perfil_usuario'),
    
	path('reportar/<int:noticia_id>/', views.reportar_noticia, name='reportar_noticia'),
	
	path('denuncias/', views.denuncias, name='denuncias'),
    
	path('gestionar/<int:id>/', views.gestionar_denuncia, name='gestionar_denuncia'),
    
	path('eliminar/<int:id>/', views.eliminar_denuncia, name='eliminar_denuncia'),
    
    path('bloquear_usuario/<int:user_id>/', views.bloquear_usuario, name='bloquear_usuario'),
	
]
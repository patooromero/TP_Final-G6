from django.db import models
from apps.usuarios.models import Usuario
from django.contrib.auth.models import User

class Categoria(models.Model):
	nombre = models.CharField(max_length = 60)

	def __str__(self):
		return self.nombre

class Noticia(models.Model):

	titulo = models.CharField(max_length = 150)
	cuerpo = models.TextField()
	imagen = models.ImageField(upload_to = 'noticias')
	categoria_noticia = models.ForeignKey(Categoria, on_delete = models.CASCADE)
	fecha = models.DateTimeField(auto_now_add=True)
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

	def __str__(self):
		return self.titulo
	
	
class Perfil(models.Model):
	usuario = models.OneToOneField(Usuario, null=True, on_delete = models.CASCADE)
	bio = models.TextField()
	imagen = models.ImageField(upload_to = 'perfiles', null = True, blank = True)

	def __str__(self):
		return str(self.usuario)
class Comentario(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE)
	texto = models.TextField(max_length = 1500)
	noticia = models.ForeignKey(Noticia, on_delete = models.CASCADE)
	fecha = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.noticia.titulo}->{self.texto}"
	
class Denuncia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario que realiza la denuncia
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)  # Noticia denunciada
    razon = models.TextField()  # Motivo de la denuncia
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de creación de la denuncia

    def __str__(self):
        return f'Denuncia de {self.usuario} sobre {self.noticia}'
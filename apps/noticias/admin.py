from django.contrib import admin
from .models import Categoria, Noticia, Perfil, Denuncia

admin.site.register(Categoria)
admin.site.register(Noticia)
admin.site.register(Perfil)
admin.site.register(Denuncia)
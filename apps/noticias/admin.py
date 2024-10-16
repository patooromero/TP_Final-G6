from django.contrib import admin
from .models import Noticia, Categoria, Comentario

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'categoria_noticia')
    search_fields = ('titulo',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'noticia', 'fecha')
    search_fields = ('noticia__titulo',)

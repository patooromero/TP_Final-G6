from django import forms
from .models import Noticia, Categoria

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ('titulo', 'cuerpo', 'categoria_noticia', 'imagen')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'cuerpo': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria_noticia': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'})
        }
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
        # widgets = {
        #     'nome': forms.TextInput(attrs={'class': 'form-control'}),
        # }
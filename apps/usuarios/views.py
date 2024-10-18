from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import RegistroForm, CustomAuthenticationForm
# Create your views here.

class Registro(CreateView):
	#FORMULARIO DJANGO
	form_class = RegistroForm
	success_url = reverse_lazy('login')
	template_name = 'usuarios/registro.html'

	# Vista de login personalizada
class CustomLoginView(LoginView):
    # Usar el formulario de autenticación personalizado que verifica si el usuario está bloqueado
    form_class = CustomAuthenticationForm
    template_name = 'usuarios/login.html'
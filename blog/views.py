from django.contrib.auth import logout
from django.shortcuts import render, redirect

#request 'es un diccionario que continuamente se va pasando entre el navegador y el servidor'

def Home(request):

	return render(request, 't_home.html')


def Nosotros(request):

	return render(request, 't_nosotros.html')

def logout_view(request):
    logout(request)
    return redirect('home')

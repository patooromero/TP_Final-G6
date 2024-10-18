from django.urls import path
from .views import Registro, CustomLoginView

from . import views

app_name = 'usuarios'

urlpatterns = [
    
    path('registro/', views.Registro.as_view(), name = 'registro'),
    path('login/', CustomLoginView.as_view(), name='login'),

]
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from .models import Usuario
from django.utils.translation import gettext_lazy as _

class RegistroForm(UserCreationForm):
    email = forms.EmailField(label='Correo', required=True)
    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellido', required=True)
    password1 = forms.CharField(
        label='Contraseña', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(
        label='Confirmar Contraseña', widget=forms.PasswordInput, required=True)

    class Meta:
        model = Usuario
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]
        help_texts = {
            'username': None,
        }

# # Formulario de autenticación personalizado para mostrar mensaje de usuario bloqueado
# class CustomAuthenticationForm(AuthenticationForm):

#     def confirm_login_allowed(self, user):
#         if not user.is_active:
#             raise ValidationError(
#                 "Este usuario está bloqueado.",
#                 code='inactive',
#             )

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("Este usuario está bloqueado."),
                code='inactive',
            )
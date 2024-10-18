from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Noticia, Categoria, Comentario, Denuncia
from .forms import NoticiaForm, CategoriaForm, DenunciaForm
from apps.usuarios.models import Usuario


@login_required
def Crear_Categoria(request):
	contexto = {'form': CategoriaForm()}
	if request.method == 'POST':
		form = CategoriaForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('noticias:crear_categoria')
		else:
			contexto['form'] = form
	return render(request, 'noticias/crear_categoria.html', contexto)

@login_required
def Crear_Noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.usuario = request.user
            noticia.save()
            return redirect('noticias:listar')
        else:
            print(form.errors)
    else:
        form = NoticiaForm()
    
    return render(request, 'noticias/crear.html', {'form': form})

# @login_required
def Listar_Noticias(request):
	contexto = {}
	id_categoria = request.GET.get('id',None)
	if id_categoria:
		n = Noticia.objects.filter(categoria_noticia = id_categoria)
	else:
		n = Noticia.objects.all() #RETORNA UNA LISTA DE OBJETOS
	contexto['noticias'] = n
	cat = Categoria.objects.all().order_by('nombre')
	contexto['categorias'] = cat
	return render(request, 'noticias/listar.html', contexto)

# @login_required
def Detalle_Noticias(request, pk):
	contexto = {}
	n = Noticia.objects.get(pk = pk) #RETORNA SOLO UN OBEJTO
	contexto['noticia'] = n
	c = Comentario.objects.filter(noticia = n)
	contexto['comentarios'] = c
	return render(request, 'noticias/detalle.html',contexto)


@login_required
def Comentar_Noticia(request):
	com = request.POST.get('comentario',None)
	usu = request.user
	noti = request.POST.get('id_noticia', None)# OBTENGO LA PK
	noticia = Noticia.objects.get(pk = noti) #BUSCO LA NOTICIA CON ESA PK
	coment = Comentario.objects.create(usuario = usu, noticia = noticia, texto = com)

	return redirect(reverse_lazy('noticias:detalle', kwargs={'pk': noti}))

@login_required
def delete_comment(request, comment_id):
    comentario = get_object_or_404("Aqui_va_el_modelo_de_comentario", pk=comment_id)
    if comentario.usuario == request.user:
        comentario.delete()   
        return redirect(reverse_lazy('noticias:home'))
    else:
        # Manejar el caso en el que el usuario intenta eliminar un comentario que no es suyo
        # Por ejemplo, mostrar un mensaje de error
        return render(request, 'error.html')

@login_required
def eliminar_noticia(request, pk):
    noticia = Noticia.objects.get(pk=pk)
    if request.user == noticia.usuario:
        noticia.delete()
        return redirect('noticias:listar')
    else:
        return render(request, 'noticias/error.html', {'mensaje': 'No tienes permiso para eliminar esta noticia'})

@login_required
def perfil_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    n =Usuario.objects.all() #RETORNA UNA LISTA DE OBJETOS
    contexto = {'usuario': usuario, 'lista_usuarios': n}
    return render(request, 'noticias/perfil_usuario.html', contexto)

@login_required    
def reportar_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            denuncia = form.save(commit=False)
            denuncia.usuario = request.user  # Asegúrate de que el usuario esté autenticado
            denuncia.noticia = noticia
            denuncia.save()
            messages.success(request, 'Tu denuncia ha sido enviada con éxito.') #mensaje de que se guardo la denuncia
            return redirect('noticias:detalle', pk=noticia.id)  # Redirige a la vista de detalle de la noticia
    else:
        form = DenunciaForm()
    return render(request, 'noticias/reportar_noticia.html', {'form': form, 'noticia': noticia})

@login_required
def denuncias(request):
    denuncias = Denuncia.objects.all()  # Obtén todas las denuncias
    return render(request, 'noticias/denuncias.html', {'denuncias': denuncias})

@login_required
def gestionar_denuncia(request, id):
    denuncia = get_object_or_404(Denuncia, id=id)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'aprobar':
            # Lógica para aprobar la denuncia
            messages.success(request, 'Denuncia aprobada.')
        elif accion == 'rechazar':
            # Lógica para rechazar la denuncia
            messages.error(request, 'Denuncia rechazada.')
        return redirect('noticias:denuncias')
    return render(request, 'noticias/gestion_denuncia.html', {'denuncia': denuncia})

@login_required
def eliminar_denuncia(request, id):
    # Obtener la denuncia o mostrar 404 si no existe
    denuncia = get_object_or_404(Denuncia, id=id)
    if request.method == 'POST':
        # Eliminar la denuncia
        denuncia.delete()
        messages.success(request, 'Denuncia eliminada con éxito.')
        return redirect('noticias:denuncias')  # Redirigir a la lista de denuncias
    # Si no es un POST, probablemente querías mostrar un mensaje de confirmación
    return render(request, 'noticias/confirmar_eliminacion.html', {'denuncia': denuncia})

# Asegurarse de que solo los superusuarios puedan acceder
@user_passes_test(lambda u: u.is_superuser)
def bloquear_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if usuario.is_active:
        usuario.is_active = False
        usuario.save()
        messages.success(request, f'El usuario {usuario.username} ha sido bloqueado.')
    else:
        messages.warning(request, f'El usuario {usuario.username} ya estaba bloqueado.')
    
    return redirect('noticias:perfil_usuario', request.user.pk)




#{'nombre':'name', 'apellido':'last name', 'edad':23}
#EN EL TEMPLATE SE RECIBE UNA VARIABLE SEPARADA POR CADA CLAVE VALOR
# nombre
# apellido
# edad

'''
ORM

CLASE.objects.get(pk = ____)
CLASE.objects.filter(campos = ____)
CLASE.objects.all() ---> SELECT * FROM CLASE

'''

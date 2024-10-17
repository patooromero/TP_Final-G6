from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Noticia, Categoria, Comentario
from .forms import NoticiaForm, CategoriaForm
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

# @login_required
# def perfil_usuario_list(request, pk):
#     usuario = get_object_or_404(Usuario, pk=pk)
#     usuarios = Usuario.objects.all()
#     contexto = {'usuario': usuario, 'usuarios': usuarios}
#     return render(request, 'noticias/perfil_usuario.html', contexto)



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

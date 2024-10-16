from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Noticia, Categoria, Comentario
from .forms import NoticiaForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


def Listar_Noticias(request):
    contexto = {}

    id_categoria = request.GET.get('id', None)

    if id_categoria:
        n = Noticia.objects.filter(categoria_noticia=id_categoria)
    else:
        n = Noticia.objects.all()  # Retorna una lista de objetos

    contexto['noticias'] = n
    cat = Categoria.objects.all().order_by('nombre')
    contexto['categorias'] = cat

    return render(request, 'noticias/listar.html', contexto)

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


def Detalle_Noticias(request, pk):
    contexto = {}

    try:
        n = Noticia.objects.get(pk=pk)
        contexto['noticia'] = n

        c = Comentario.objects.filter(noticia=n)
        contexto['comentarios'] = c

        return render(request, 'noticias/detalle.html', contexto)

    except Noticia.DoesNotExist:
        return render(request, 'noticias/no_encontrado.html', {})


@login_required
def Comentar_Noticia(request):
    com = request.POST.get('comentario', None)
    usu = request.user
    noti = request.POST.get('id_noticia', None)  # OBTENGO LA PK
    noticia = Noticia.objects.get(pk=noti)  # BUSCO LA NOTICIA CON ESA PK
    Comentario.objects.create(usuario=usu, noticia=noticia, texto=com)

    return redirect(reverse_lazy('noticias:detalle', kwargs={'pk': noti}))

@login_required
def Eliminar_Comentario(request, pk):
    if request.method == 'POST':
        comentario = get_object_or_404(Comentario, pk=pk)  # Busca el comentario por su pk
        if comentario.usuario == request.user:  # Verifica que el usuario sea el dueño del comentario
            comentario.delete()  # Elimina el comentario
            return redirect('noticias:listar')  # Redirige a la lista de noticias o donde desees
    return redirect('noticias:listar')  # Redirige en caso de un acceso no permitido


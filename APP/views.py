from django.shortcuts import render, redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.conf import Settings
from django.urls import reverse_lazy , reverse

from django.shortcuts import get_object_or_404
from APP.models import *
from APP.forms import *
from django.contrib import messages

from django.views.generic import ListView , DetailView
from django.views.generic.edit import CreateView , DeleteView , UpdateView

from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login , authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin


# Create your views here.

def inicio(request):
    return render (request , "APP/inicio.html")

def nosotros (request):
    return render (request , "APP/nosotros.html")

def creadores (request):
    return render (request , "APP/creadores.html")

#*************************************

#REGISTRO

def registro (request):
    if request.method == "POST":
        miFormularioR = formulario_registro(request.POST)
        if miFormularioR.is_valid():
            miFormularioR.save()
            username = miFormularioR.cleaned_data.get("username")
            return render (request , "APP/inicio.html")

    else:
        miFormularioR = formulario_registro()
    return render (request , "APP/autenticacion/registro.html" , {"FormularioR" : miFormularioR})

#*************************************

def iniciar_sesion (request):
    if request.method == "POST":
        miFormularioR = AuthenticationForm(request , data=request.POST)
        if miFormularioR.is_valid():
            usuario = miFormularioR.cleaned_data.get("username")
            contraseña = miFormularioR.cleaned_data.get("password")
            miUsuario = authenticate(username=usuario , password=contraseña)

            if miUsuario:
                login(request , miUsuario)
                mensaje = f"Hermoso Verte {miUsuario}"
                return render (request , "APP/inicio.html" , {"mensaje":mensaje})

        else:
            mensaje = f"Error - Usuario no Encontrado"
            return render (request , "APP/inicio.html" , {"mensaje":mensaje})

    else:
        miFormularioR = AuthenticationForm()

    return render (request , "APP/autenticacion/login.html" , {"FormularioR" : miFormularioR})


#*************************************
#PERFIL***********

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST , request.FILES , instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Se Actualizó!')
            return redirect("Profile_P")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form , "p_form": p_form}
    return render(request, "APP/profile.html", context)




#LIKE PUBLICACION***********

def LikeView (request , pk):
    Posteo = get_object_or_404 (posteo , id=request.POST.get("posteo_id"))
    Posteo.likes.add (request.user)
    return HttpResponseRedirect (reverse ("Post-detail" , args=[str(pk)]))



#COMENTARIO EN PUBLICACION***********

class AddComentView (LoginRequiredMixin , CreateView):
    model = Coment
    #form_class = AddComentForm
    template_name = "APP/add_coment.html"
    fields = ["name" , "body"]
    success_url = "/APP/post/ver"

    def form_valid(self, form):
        form.instance.posteo_id = self.kwargs["pk"]
        return super().form_valid(form)



#*********PUBLICACIONES*********

#NUEVA

class nuevoposteo (LoginRequiredMixin , CreateView):
    model = posteo
    form_class = PostForm

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


#VER LISTA

class verPostView (LoginRequiredMixin , ListView):
    model = posteo
    template_name = "APP/posteo_list.html"
    ordering = ["-post_date"]
 #   ordering = ["-id"]


#VER PUBLICACION

class artDetailView (LoginRequiredMixin , DetailView):
    model = posteo
    template_name = "APP/posteo_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(artDetailView , self).get_context_data(*args, **kwargs)
        cant_like = get_object_or_404 (posteo , id=self.kwargs["pk"])
        total_likes = cant_like.total_likes()
        context ["total_likes"] = total_likes
        return context


#ACTUALIZAR PUBLICACION

class UpdatePost (LoginRequiredMixin , UserPassesTestMixin , UpdateView):
    model = posteo
    fields = ["titulo" , "body"]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        posteo =  self.get_object()
        if self.request.user == posteo.autor:
            return True
        return False 


#DELETE PUBLICACION

class delte_Post (LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = posteo
    success_url = "/APP/post/ver"
    
    def test_func(self):
        posteo =  self.get_object()
        if self.request.user == posteo.autor:
            return True
        return False 


###########################
def historia_m (request):
        historia_m = f"Hermoso Verte"
        return render  (request, "APP/inicio.html" , {"historia_m":historia_m})


#instance=request.posteo.body
#*********SITIOS*********


class crear_lugar_interes (LoginRequiredMixin , CreateView):
    model = sitios 
    fields = ["pais" , "ciudad" , "direccion" , "actividad_paranormal" , "datos"]
    success_url = "/APP/sitios/lista"

class lista_lugar_interes (LoginRequiredMixin , ListView):
    model = sitios
    template_name = "APP/sitios_lista.html"

class delte_lugar_interes (LoginRequiredMixin , UserPassesTestMixin , DeleteView):
    model = sitios
    success_url = "/APP/sitios/lista"

    def test_func(self):
        posteo =  self.get_object()
        if self.request.user.is_superuser:
            return True
        return False 

class editar_lugar_interes (LoginRequiredMixin , UserPassesTestMixin , UpdateView):
    model = sitios
    fields = ["pais" , "ciudad" , "direccion" , "actividad_paranormal" , "datos"]
    success_url = "/APP/sitios/lista"

    def test_func(self):
        posteo =  self.get_object()
        if self.request.user.is_superuser:
            return True
        return False 


def busqueda_lugar (request):
    return render (request , "APP/Busqueda_s.html")


def result_busqueda_sitio (request):
    if request.method == "GET":
        busqueda_s = request.GET["pais"]
        resultado_s = sitios.objects.filter(pais__icontains = busqueda_s)
        return render (request , "APP/ResultadoBusqueda_s.html" , {"Pais":resultado_s , "resultado":resultado_s})

    return render (request , "APP/ResultadoBusqueda_s.html")
from django.urls import path
from APP.views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('inicio/', inicio , name= "Inicio"),
    path('', inicio , name= "Inicio"),

    path('uss/', nosotros , name="Nosotros"),
    path('creadores_/', creadores , name="Creadores"),


    path('registro_/', registro , name="Sign up"),
    path('login_/', iniciar_sesion , name="Sign in"),
    path('logout/', LogoutView.as_view(template_name="APP/autenticacion/logout.html") , name="Logout"),

    path('profile_p/', profile , name="Profile_P"),

    path('post/nuevo', nuevoposteo.as_view() , name="Nuevo-Post"),
    path('post/ver', verPostView.as_view() , name="Post"),
    path('post/<int:pk>', artDetailView.as_view() , name="Post-detail"),
    path('post/edit/<int:pk>', UpdatePost.as_view() , name="Post-Edit"),
    path('post/borrar/<int:pk>', delte_Post.as_view() , name="Post-Delete"),


    path('like/<int:pk>', LikeView , name="like_post"),
    path('post/<int:pk>/coment', AddComentView.as_view() , name="Nuevo-Coment"),


    path('sitios/nuevo', crear_lugar_interes.as_view() , name="Crear Sitio"),
    path('sitios/lista', lista_lugar_interes.as_view() , name="Ver Lista Sitio"),
    path('sitios/borrar/<int:pk>', delte_lugar_interes.as_view() , name="Borrar Sitio"),
    path('sitios/edit/<int:pk>', editar_lugar_interes.as_view() , name="Editar Sitio"),

    path('search_site/', busqueda_lugar , name="Search Site"),
    path('dato_site/', result_busqueda_sitio , name="Data Site"),


]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

from django.conf.urls import url
from django.contrib import admin

from . import views

app_name = "embriologia"

urlpatterns = [	
    url(r'^$', views.index, name='index'), 
    url(
    	r'^lista/(?:(?P<periodo>[0-9]+)/(?P<pageIndex>[0-9]+)/(?P<pageSize>[0-9]+)/)?$', 
    	views.listaEm,
    	name='lista'
    ),
    url(
        r'^listaSem/(?:(?P<periodo>[0-9]+)/(?P<pageIndex>[0-9]+)/(?P<pageSize>[0-9]+)/)?$', 
        views.listaSem,
        name='listaSem'
    ),
    url(r'^eliminar/(?P<id>[0-9]+)$', views.eliminar, name="eliminar"),
    url(
        r'^guardar/(?:(?P<id>[0-9]+)/(?P<tipo>[0-9]+)/)?$', 
        views.guardar, 
        name="guardar"
    ),
    url(r'^ver/([0-9]+)/$', views.ver, name="ver"),
    url(r'^comentar/$', views.comentar, name="comentar"),
    url(r'^upload/$', views.upload, name="upload"),
     url(
        r'^modificar/(?:(?P<id>[0-9]+)/(?P<tipo>[0-9]+)/)?$', 
        views.modificar, 
        name="modificar"
    ),
]

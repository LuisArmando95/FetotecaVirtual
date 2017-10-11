from django.conf.urls import url
from . import views

app_name = "usuarios"

urlpatterns = [	
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^signup$', views.registro, name='registro'),
	url(r'^cambioContra$', views.cambioContra, name='cambioContra'),
	url(r'^cambioCorreo$', views.cambioCorreo, name='cambioCorreo'),
]
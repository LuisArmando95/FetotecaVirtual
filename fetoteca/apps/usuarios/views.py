# -*- coding: utf-8 -*
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse 
from django.contrib import auth
from .models import Usuario
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

import json


def postcondition(post_cond):
	def decorator(view_func):
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			result = view_func(request, *args, **kwargs)
			post_cond(request)
			return result
		return _wrapped_view
	return decorator

def delete_session_message(request):
	if 'message' in request.session:
		del request.session['message']


# Create your views here.
def login(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username = username, password = password)
	if user is not None and user.is_active:
		auth.login(request, user)
		result = {'status':'ok','type': 'success', 'description': 'Bienvenid@ ' + user.get_full_name()}
	else:
		result = {'status':'error','type': 'danger', 'description': 'Usuario o contraseña incorrecta'}

	if request.content_type == 'application/json':
		return HttpResponse(json.dumps(result), mimetype='application/json')
	else:
		source = request.POST.get('source', reverse('embriologia:index'))
		request.session['message'] = result;
		return redirect(source)

def logout(request):
	auth.logout(request)
	return redirect(reverse('embriologia:index'))

def cambioCorreo(request):
	if request.method == 'POST':
		try:

			email = request.POST.get('email', '')
			prueba= User.objects.get(username= request.user.get_username())
			username= prueba.get_username()
			if User.objects.filter(email=email).count():
				raise Exception('Este email ya existe con otro usuario. Intenta con otro.')
			send_mail("Cambio de correo en la Fetoteca Virtual", 
          		"Se ha asociado este correo con el usuario: "+ username, 
          		'"Fetoteca Virtual." <fetoteca.virtual.uaz@gmail.com>',
          		[email])
			
			prueba.email=email

			prueba.save()
			

			request.session['message'] = {'status': 'ok', 'type':'success', 'description': 'Correo actualizado satisfactoriamente'}
			return redirect(reverse('embriologia:index'))
		except Exception as error:
			request.session['message'] = {'status':'error', 'type':'danger','description': error.message}
			return redirect(reverse('usuarios:cambioCorreo'))
	else:
		context = {}
		context['source'] = reverse('embriologia:index')
		context['breadcrumb'] = [ 
			("Inicio", reverse("embriologia:index")) ,
			("Cambiar correo", '#')
		]
		return render(request, 'cambiar_correo.html', context)

def cambioContra(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!

			traerusuario= User.objects.get(username= request.user.get_username())
			username= traerusuario.get_username()
			
			traerusuario.email_user("Cambio de Contrasena", "Se ha cambiado la contrasena del usuario: "+ username)

			messages.success(request, '¡Tu contraseña ha sido actualizada exitosamente!')
			return redirect(reverse('embriologia:index'))
		else:
			messages.error(request, 'Datos incorrectos, por favor ingresa los datos solicitados correctamente.')
	else:
		form = PasswordChangeForm(request.user)
		
	return render(request, 'cambiar_contraseña.html', {
		'form': form
	})
	


def registro(request):
	if request.method == 'POST':
		try:
			username = request.POST.get('username', '')
			password = request.POST.get('password', '')
			password_confirmation = request.POST.get('password_confirmation', '')
			firstname = request.POST.get('firstname', '')
			lastname = request.POST.get('lastname', '')
			email = request.POST.get('email', '')
			sexo = request.POST.get('sexo', '')

			if firstname == "":
				raise Exception('El nombre no puede estar vacío.')
			if lastname == "":
				raise Exception('El apellido no puede estar vacío.')
			if sexo == "":
				raise Exception("Debes seleccionar un sexo.")
			if username == "":
				raise Exception("Usuario(nick) es un campo obligatorio.")
			if password  == "":
				raise Exception('La contraseña es un campo obligatorio.')
			if password != password_confirmation or password == "":
				raise Exception('Los campos contraseña y confirmar contraseña son diferentes.')

			
			if User.objects.filter(username=username).count():
				raise Exception('Este Usuario(nick) ya existe. Intenta con otro.')
			if User.objects.filter(email=email).count():
				raise Exception('Este email ya existe con otro usuario. Intenta con otro.')

			user = User.objects.create_user(username, email, password)
			user.last_name = lastname
			user.first_name = firstname


			group = Group.objects.get(name="Estudiantes")
			user.groups.add(group)
			user.save()

			

			profile = Usuario()
			profile.user = user
			profile.sexo = sexo
			profile.save()
			
			send_mail("Bienvenido a la Fetoteca Virtual", 
          		"Bienvenido '"+ firstname+" " +lastname+ "' a la Fetoteca Virtual" +"\nUsuario: "+ username, 
          		'"Fetoteca Virtual." <fetoteca.virtual.uaz@gmail.com>',
          		[email])

			request.session['message'] = {'status': 'ok', 'type':'success', 'description': 'Perfil creado satisfactoriamente'}
			return redirect(reverse('embriologia:index'))
		except Exception as error:
			request.session['message'] = {'status':'error', 'type':'danger','description': error.message}
			return redirect(reverse('usuarios:registro'))
	else:
		context = {}
		context['source'] = reverse('embriologia:index')
		context['breadcrumb'] = [ 
			("Inicio", reverse("embriologia:index")) ,
			("Registro", '#')
		]
		return render(request, 'usuario_registro.html', context)



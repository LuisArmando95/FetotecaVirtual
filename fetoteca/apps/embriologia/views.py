# -*- coding: utf-8 -*
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.urls import reverse, reverse_lazy
from .models import Feto, Malformacion, ImagenFeto, PeriodoPrenatal, Comentario, Semestre
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template import loader, Context
from functools import wraps
from django.utils.decorators import available_attrs
import json
import pprint
import cgi
import time
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from os import listdir
from os.path import isfile, join
from django.conf import settings

from django.contrib.staticfiles.templatetags.staticfiles import static

default_source = reverse_lazy('embriologia:index')

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

@postcondition(delete_session_message)
def listaEm(request, periodo, pageIndex, pageSize):
	if periodo is None:
		periodo = 0
	if pageIndex is None:
		pageIndex = 1
	if pageSize is None:
		pageSize = 6
		
	periodo = int(periodo)
	pageIndex = int(pageIndex)
	pageSize = int(pageSize)
	if pageSize < 6 or pageSize > 12:
		pageSize = 0
	filter = None
	filterSet = request.POST.get('filter', request.GET.get('filter', ''))
	

	# Filtramos por periodo prenatal (1, 2)
	if periodo >= 1000:
		filter = Q(tipo__gte = 1)
	elif periodo > 0: 
		filter = Q(periodo__id = periodo, tipo = 0)
	else:
		filter = Q(tipo = 0)
	# Filtramos por malformacion
	if filterSet:
		filterSet = filterSet.split('_')
		filter = filter & Q(malformaciones__id__in = filterSet)
	fetos = Feto.objects.filter(filter).distinct()

	# Filtramos por semestre
	


	if pageSize == 0:
		if fetos.count() == 0:
			paginator = Paginator(fetos, 1)
		else:
			paginator = Paginator(fetos, fetos.count())
	else:
		paginator = Paginator(fetos, pageSize)

	try:
		fetos = paginator.page(pageIndex)
	except EmptyPage:
		fetos = paginator.page(paginator.num_pages)

	context = Context({'request': request})
	context['source'] = reverse('embriologia:lista', kwargs={'periodo':periodo, 'pageIndex':pageIndex, 'pageSize':pageSize})
	context['breadcrumb'] = [ ("Inicio", reverse("embriologia:index")) ,("Embriología" if periodo < 1000 else "Trabajos Científicos", "#") ]
	context['fetos'] = fetos
	context['malformaciones'] = Malformacion.objects.all()
	context['malformacionesSeleccionadas'] = filterSet
	
	context['periodos'] = PeriodoPrenatal.objects.all()
	context['periodoSeleccionado'] = periodo
	context['pageSize'] = pageSize
	context['totalResults'] = Feto.objects.all().count()
	if periodo >= 1000:
		return render(request, 'documento_lista.html', context)
	else:
		return render(request, 'embriologia_lista.html', context)

@postcondition(delete_session_message)
def listaSem(request, periodo, pageIndex, pageSize):
	if periodo is None:
		periodo = 0
	if pageIndex is None:
		pageIndex = 1
	if pageSize is None:
		pageSize = 6
		
	periodo = int(periodo)
	pageIndex = int(pageIndex)
	pageSize = int(pageSize)
	if pageSize < 6 or pageSize > 12:
		pageSize = 0
	filter = None

	# Filtramos por periodo prenatal (1, 2)
	if periodo >= 1000:
		filter = Q(tipo__gte = 1)
	elif periodo > 0: 
		filter = Q(periodo__id = periodo, tipo = 0)
	else:
		filter = Q(tipo = 0)

	# Filtramos por semestre
	
	filterSet2 = request.POST.get('filter', request.GET.get('filter', ''))
	if filterSet2:
	 	filterSet2 = filterSet2.split('_')
		filter = filter & Q(semestres__id__in = filterSet2)
	fetos = Feto.objects.filter(filter).distinct()

	if pageSize == 0:
		if fetos.count() == 0:
			paginator = Paginator(fetos, 1)
		else:
			paginator = Paginator(fetos, fetos.count())
	else:
		paginator = Paginator(fetos, pageSize)

	try:
		fetos = paginator.page(pageIndex)
	except EmptyPage:
		fetos = paginator.page(paginator.num_pages)

	context = Context({'request': request})
	context['source'] = reverse('embriologia:listaSem', kwargs={'periodo':periodo, 'pageIndex':pageIndex, 'pageSize':pageSize})
	context['breadcrumb'] = [ ("Inicio", reverse("embriologia:index")) ,("Embriología" if periodo < 1000 else "Trabajos Científicos", "#") ]
	context['fetos'] = fetos
	
	context['semestres'] = Semestre.objects.all()
	context['semestresSeleccionados'] = filterSet2
	context['periodos'] = PeriodoPrenatal.objects.all()
	context['periodoSeleccionado'] = periodo
	context['pageSize'] = pageSize
	context['totalResults'] = Feto.objects.all().count()
	if periodo >= 1000:
		return render(request, 'documento_lista.html', context)
	else:
		return render(request, 'embriologia_lista.html', context)
# @lista/semana/pageIndex/pageSize?filter=filtros_seleccionados
@postcondition(delete_session_message)
def lista(request, periodo, pageIndex, pageSize):
	if periodo is None:
		periodo = 0
	if pageIndex is None:
		pageIndex = 1
	if pageSize is None:
		pageSize = 6
		
	periodo = int(periodo)
	pageIndex = int(pageIndex)
	pageSize = int(pageSize)
	if pageSize < 6 or pageSize > 12:
		pageSize = 0
	filter = None
	filterSet = request.POST.get('filter', request.GET.get('filter', ''))
	

	# Filtramos por periodo prenatal (1, 2)
	if periodo >= 1000:
		filter = Q(tipo__gte = 1)
	elif periodo > 0: 
		filter = Q(periodo__id = periodo, tipo = 0)
	else:
		filter = Q(tipo = 0)
	# Filtramos por malformacion
	if filterSet:
		filterSet = filterSet.split('_')
		filter = filter & Q(malformaciones__id__in = filterSet)
	fetos = Feto.objects.filter(filter).distinct()

	# Filtramos por semestre
	
	filterSet2 = request.POST.get('filter', request.GET.get('filter', ''))
	if filterSet2:
	 	filterSet2 = filterSet2.split('_')
		filter = filter & Q(semestres__id__in = filterSet2)
	fetos = Feto.objects.filter(filter).distinct()

	if pageSize == 0:
		if fetos.count() == 0:
			paginator = Paginator(fetos, 1)
		else:
			paginator = Paginator(fetos, fetos.count())
	else:
		paginator = Paginator(fetos, pageSize)

	try:
		fetos = paginator.page(pageIndex)
	except EmptyPage:
		fetos = paginator.page(paginator.num_pages)

	context = Context({'request': request})
	context['source'] = reverse('embriologia:lista', kwargs={'periodo':periodo, 'pageIndex':pageIndex, 'pageSize':pageSize})
	context['breadcrumb'] = [ ("Inicio", reverse("embriologia:index")) ,("Embriología" if periodo < 1000 else "Trabajos Científicos", "#") ]
	context['fetos'] = fetos
	context['malformaciones'] = Malformacion.objects.all()
	context['malformacionesSeleccionadas'] = filterSet
	context['semestres'] = Semestre.objects.all()
	context['semestresSeleccionados'] = filterSet2
	context['periodos'] = PeriodoPrenatal.objects.all()
	context['periodoSeleccionado'] = periodo
	context['pageSize'] = pageSize
	context['totalResults'] = Feto.objects.all().count()
	if periodo >= 1000:
		return render(request, 'documento_lista.html', context)
	else:
		return render(request, 'embriologia_lista.html', context)

@postcondition(delete_session_message)
def index(request):
	context = {}
	context['source'] = reverse('embriologia:index')
	context['breadcrumb'] = [ ("Inicio", reverse("embriologia:index")) ,("Fetoteca Virtual", default_source) ]
	images = []
	#path = '.' + static('index_gallery')
	path = settings.BASE_DIR + static('index_gallery')
	for file in listdir(path):
		if isfile(join(path, file)):
			images.append(join('index_gallery', file))
	context['images'] = images

	return render (request,'index.html',context)

def eliminar(request, id):
	if not (request.user.is_authenticated() and request.user.has_perm('embriologia.delete_feto')):
		result = {'status': 'error', 'description':'No tienes permisos para borrar fetos', 'type': 'danger'}
	else:
		result = {'status': '', 'description':''}
		try:
			feto = Feto.objects.get(pk=id)
			feto.delete()
			result['status'] = 'ok'
			result['description'] = 'El registro ha sido eliminado con éxito'
			result['type'] = 'success'
		except ObjectDoesNotExist:
			result['status'] = 'error'
			result['type'] = 'danger'
			result['description'] = 'El identificador del feto no es válido, no se pudo eliminar'
	
	if request.content_type == 'application/json':
		return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		request.session['message'] = result
		source = request.GET.get('source', request.POST.get('source', default_source))
		return redirect(source)


@postcondition(delete_session_message)
def guardar(request, id, tipo):
	if id is None:
		id = '0'
	if tipo is None:
		tipo = 0
	else:
		tipo = int(tipo)
	#Mostramos solo la informacion de un registro si el metodo es GET

	if request.method == 'GET':
		context = {}
		context['breadcrumb'] = [ 
			("Inicio", reverse("embriologia:index")) ,
			("Embriología" if tipo == 0 else "Trabajos Científicos", reverse('embriologia:listaSem') if tipo == 0 else reverse('embriologia:listaSem', args=(1000, 0, 12))),
			("Crear" if id=='0' else "Modificar", "#")
		]
		if id != '0':
			context['feto'] = get_object_or_404(Feto, pk=id)
		context['periodos'] = PeriodoPrenatal.objects.all()
		context['malformaciones'] = Malformacion.objects.all()
		context['semestres'] = Semestre.objects.all()
		if tipo == 0:
			return render(request, 'embriologia_guardar.html', context)
		else:
			return render(request,'documento_guardar.html', context)
	#Cuando el metodo es POST guardamos la informacion que viene a traves
	#del cuerpo de la solicitud
	elif request.method == 'POST':
		if not (request.user.is_authenticated() and request.user.has_perm('embriologia.add_feto')):
			result = {'status': 'error', 'description':'No tienes permisos para agregar fetos', 'type': 'danger'}
		else:
			doc = json.loads(request.body.decode('utf-8'))
			if 'id' in doc:
				try:
					feto = Feto.objects.get(pk=doc['id'])
				except ObjectDoesNotExist:
					result = {'status':'error', 'description':'El id del registro no existe'}
					return HttpResponse(json.dumps(result), content_type='application/json')
				if request.user != feto.creator:
					result = {'status':'error', 'description': 'No eres dueño de este documento, no puedes editarlo'}
			else:
				feto = Feto()

			feto.nombre = doc['title']
			if 'description' in doc:
				feto.descripcion = doc['description'] 
			feto.contenido = doc['content']
			if 'period' in doc:
				feto.periodo = PeriodoPrenatal.objects.get(pk=doc['period'])
			if 'type' in doc:
				feto.tipo = doc['type']
			else:
				feto.tipo = 0
			feto.creator = request.user
			feto.save()
			if 'malformations' in doc:
				feto.malformaciones = doc['malformations']
			if 'semester' in doc:
				feto.semestres = doc['semester']
			if 'images' in doc and len(doc['images']) > 0: 
				feto.imagenes = doc['images'];
			result = {'status': 'ok', 'description':'Registro guardado con éxito', 'type': 'success', 'id':feto.id}

		return HttpResponse(json.dumps(result), content_type='application/json')
	return redirect(reverse('embriologia:index'))


@postcondition(delete_session_message)
def modificar(request, id, tipo):
	if id is None:
		id = '0'
	if tipo is None:
		tipo = 0
	else:
		tipo = int(tipo)
	#Mostramos solo la informacion de un registro si el metodo es GET

	if request.method == 'GET':
		context = {}
		context['breadcrumb'] = [ 
			("Inicio", reverse("embriologia:index")) ,
			("Embriología" if tipo == 0 else "Trabajos Científicos", reverse('embriologia:listaSem') if tipo == 0 else reverse('embriologia:listaSem', args=(1000, 0, 12))),
			("Crear" if id=='0' else "Modificar", "#")
		]
		if id != '0':
			context['feto'] = get_object_or_404(Feto, pk=id)
		context['periodos'] = PeriodoPrenatal.objects.all()
		context['malformaciones'] = Malformacion.objects.all()
		context['semestres'] = Semestre.objects.all()
		if tipo == 0:
			return render(request, 'embriologia_modificar.html', context)
		else:
			return render(request,'documento_modificar.html', context)
	#Cuando el metodo es POST guardamos la informacion que viene a traves
	#del cuerpo de la solicitud
	elif request.method == 'POST':
		if not (request.user.is_authenticated() and request.user.has_perm('embriologia.add_feto')):
			result = {'status': 'error', 'description':'No tienes permisos para agregar fetos', 'type': 'danger'}
		else:
			doc = json.loads(request.body.decode('utf-8'))
			if 'id' in doc:
				try:
					feto = Feto.objects.get(pk=doc['id'])
				except ObjectDoesNotExist:
					result = {'status':'error', 'description':'El id del registro no existe'}
					return HttpResponse(json.dumps(result), content_type='application/json')
				if request.user != feto.creator:
					result = {'status':'error', 'description': 'No eres dueño de este documento, no puedes editarlo'}
			else:
				feto = Feto()

			feto.nombre = doc['title']
			if 'description' in doc:
				feto.descripcion = doc['description'] 
			feto.contenido = doc['content']
			if 'period' in doc:
				feto.periodo = PeriodoPrenatal.objects.get(pk=doc['period'])
			if 'type' in doc:
				feto.tipo = doc['type']
			else:
				feto.tipo = 0
			feto.creator = request.user
			feto.save()
			if 'malformations' in doc:
				feto.malformaciones = doc['malformations']
			if 'semester' in doc:
				feto.semestres = doc['semester']
			if 'images' in doc and len(doc['images']) > 0: 
				feto.imagenes = doc['images'];
			result = {'status': 'ok', 'description':'Registro guardado con éxito', 'type': 'success', 'id':feto.id}

		return HttpResponse(json.dumps(result), content_type='application/json')
	return redirect(reverse('embriologia:index'))

@postcondition(delete_session_message)
def ver(request,id):
	context = {}
	context['source'] = reverse('embriologia:ver', args = [id])
	context['periodos'] = PeriodoPrenatal.objects.all()
	context['malformaciones'] = Malformacion.objects.all()
	context['semestres'] = Semestre.objects.all()
	context['feto'] = get_object_or_404(Feto, pk=id)
	context['comentarios'] = Comentario.objects.filter(feto__id = id).order_by('-id')
	context['breadcrumb'] = [ 
		("Inicio", reverse("embriologia:index")) ,
		("Embriología", default_source),
		("Ver", '#'),
		(context['feto'].nombre, "#")
	]
	if int(context['feto'].tipo) >= 1000:
		context['breadcrumb'] = [ 
			("Inicio", reverse("embriologia:index")) ,
			("Trabajos Científicos", reverse('embriologia:listaSem', args = [1000, 0, 12] )),
			("Ver", '#'),
			(context['feto'].nombre, "#")
		]
		return render(request, 'documento_ver.html', context)
	else:
		context['breadcrumb'] = [ 
			("Inicio", reverse("embriologia:index")) ,
			("Embriología", reverse('embriologia:lista')),
			("Ver", '#'),
			(context['feto'].nombre, "#")
		]
		return render(request, 'embriologia_ver.html', context)

def comentar(request):
	if request.method == 'POST':
		if not (request.user.is_authenticated() and request.user.has_perm('embriologia.add_comentario')):
			result = {'status': 'error', 'description': 'no tienes permisos suficientes para agregar un comentario'}
		else:
			request_comment = json.loads(request.body.decode('utf-8'))
			if set(['feto', 'texto']).issubset(request_comment):
				try:
					comment = Comentario()
					comment.feto = get_object_or_404(Feto, pk=request_comment['feto']) 
					comment.texto = request_comment['texto']
					comment.user = request.user
					comment.save()
					result = {'status': 'ok', 'description': 'Comentario agregado con éxito'}
				except Exception as error:
					result = {'status': 'error', 'description': error.message, 'debug': json.dumps(request_comment)}
			else:
				result = {'status':'error', 'description': 'el campo texto y/o feto no está definido en la solicitud'}
	else:
		result = {'status':'error', 'description':'usa el método post para la solicitud'}
	if result['status'] == 'ok':
		return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		return HttpResponseBadRequest(json.dumps(result), content_type='application/json')

def upload(request):
	if request.method == 'POST':
		if not (request.user.is_authenticated()):
			result = {'status': 'error', 'description': 'No puedes subir archivos si no ingresas al sistema'};
		else:
			upload_result = []
			for key in request.FILES:
				upload_result.append(handle_upload(request.FILES[key]).id)
			result = {'status': 'ok', 'result': upload_result}
	else:
		result = {'status': 'error', 'description': 'Debes usar el método "post"'}

	return HttpResponse(json.dumps(result), content_type="application/json")


def handle_upload(file):
	image = ImagenFeto()
	milis = int(round(time.time() * 1000))
	path = 'uploads/' + str(milis) + "_" + file.name
	image.url = path
	image.save()

	#path = '.' + static(path)
	path = settings.BASE_DIR + static(path)
	
	with open(path, 'wb+') as dest:
		for chunk in file.chunks():
			dest.write(chunk)
	
	return image
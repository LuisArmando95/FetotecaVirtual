from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Malformacion(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=500)

	def __unicode__(self):
		return self.nombre

class Feto(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(null=True)
	contenido = models.TextField(null=True)
	malformaciones = models.ManyToManyField('Malformacion')
	imagenes = models.ManyToManyField('ImagenFeto')
	periodo = models.ForeignKey('PeriodoPrenatal', null=True)
	semestres = models.ManyToManyField('Semestre')
	creator = models.ForeignKey(User, null=True)
	tipo = models.IntegerField()
	def __unicode__(self):
		return self.nombre

class ImagenFeto(models.Model):
	url = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.url

class PeriodoPrenatal(models.Model):
	nombre = models.CharField(max_length=100)
	def __unicode__(self):
		return self.nombre

class Comentario(models.Model):
	texto = models.CharField(max_length=100)
	user = models.ForeignKey(User)
	feto = models.ForeignKey('Feto', on_delete=models.CASCADE)


class Semestre(models.Model):
	nombre = models.CharField(max_length=100)

	def __unicode__(self):
		return self.nombre

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Usuario(models.Model):
	user = models.ForeignKey(User)
	sexo = models.CharField(max_length=2, null=True)
	def __unicode__(self):
		return self.user.username
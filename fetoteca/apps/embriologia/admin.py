from django.contrib import admin
from .models import Feto, Malformacion, ImagenFeto, PeriodoPrenatal, Comentario, Semestre
# Register your models here.
admin.site.register(Feto)
admin.site.register(Malformacion)
admin.site.register(ImagenFeto)
admin.site.register(PeriodoPrenatal)
admin.site.register(Comentario)
admin.site.register(Semestre)
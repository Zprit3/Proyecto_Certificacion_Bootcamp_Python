from django.contrib import admin
from .models import Alumno, Instructor, Vehiculo, Practica, HistorialPractica

admin.site.register(Alumno)
admin.site.register(Instructor)
admin.site.register(Vehiculo)
admin.site.register(Practica)
admin.site.register(HistorialPractica)
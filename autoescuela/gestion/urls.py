from django.urls import path
from . import views

urlpatterns = [
    # Paneles de Administracion 
    # (Alumnos)
    path('alumnos/', views.lista_alumnos, name='lista_alumnos'),
    path('alumnos/crear/', views.crear_alumno, name='crear_alumno'),
    path('alumnos/editar/<int:alumno_id>/', views.editar_alumno, name='editar_alumno'),
    path('alumnos/eliminar/<int:alumno_id>/', views.eliminar_alumno, name='eliminar_alumno'),

    # (Instructores)
    path('instructores/', views.lista_instructores, name='lista_instructores'),
    path('instructores/crear/', views.crear_instructor, name='crear_instructor'),
    path('instructores/editar/<int:instructor_id>/', views.editar_instructor, name='editar_instructor'),
    path('instructores/eliminar/<int:instructor_id>/', views.eliminar_instructor, name='eliminar_instructor'),

    # (Vehículos)
    path('vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
    path('vehiculos/crear/', views.crear_vehiculo, name='crear_vehiculo'),
    path('vehiculos/editar/<int:vehiculo_id>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:vehiculo_id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),

    # (Prácticas)
    path('practicas/', views.lista_practicas, name='lista_practicas'),
    path('practicas/crear/', views.crear_practica, name='crear_practica'),
    path('practicas/editar/<int:practica_id>/', views.editar_practica, name='editar_practica'),
    path('practicas/eliminar/<int:practica_id>/', views.eliminar_practica, name='eliminar_practica'),

    # Panel de Administración 
    # (Gestión de Prácticas de Alumnos)
    path('gestion-practicas/<int:alumno_id>/', views.gestion_practicas_alumno, name='gestion_practicas_alumno'),
    path('gestion-practicas/editar/<int:historial_practica_id>/', views.editar_historial_practica, name='editar_historial_practica'),
    path('eliminar_practica_alumno/<int:pk>/', views.eliminar_practica_alumno, name='eliminar_practica_alumno'),
    path('lista-practicas/<int:alumno_id>/', views.lista_practicas_alumno, name='lista_practicas_alumno'),
    path('editar-practica/<int:pk>/', views.editar_practica, name='editar_practica'),
    path('practicas-instructor/', views.lista_practicas_instructor, name='lista_practicas_instructor'),
    path('mis-practicas/', views.ver_practicas_alumno, name = 'ver_practicas_alumno'),
    path('editar-practica-general/<int:pk>/', views.editar_practica_general, name='editar_practica_general'),
    path('editar-practica/<int:pk>/', views.editar_practica, name='editar_practica'),
]
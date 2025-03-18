from django.shortcuts import render, redirect
from gestion.forms import InscripcionForm
from gestion.models import Alumno, Practica, HistorialPractica
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User


def home(request):
    return render(request, 'landing/home.html')


def nosotros(request):
    return render(request, 'landing/nosotros.html')


def inscripcion(request):
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                try:
                    username = form.cleaned_data['email']
                    if User.objects.filter(username=username).exists():
                        messages.error(request, 'Ya existe un usuario con ese correo electrónico.')
                        return render(request, 'landing/inscripcion.html', {'form': form})
                    else:
                        user = User.objects.create_user(
                            username=username,
                            email=form.cleaned_data['email'],
                            password='User123456', 
                            first_name=form.cleaned_data['nombre'],
                            last_name=form.cleaned_data['apellido']
                        )
                        alumno = Alumno.objects.create(user=user, tipo_licencia=form.cleaned_data['tipo_licencia'], telefono=form.cleaned_data['telefono'])

                        practica_teorica = Practica.objects.get(tipo='teorica')
                        practica_practica = Practica.objects.get(tipo='practica')

                        HistorialPractica.objects.create(alumno=alumno, practica=practica_teorica, estado='pendiente')
                        for _ in range(2):
                            HistorialPractica.objects.create(alumno=alumno, practica=practica_practica, estado='pendiente')

                        messages.success(request, 'Su usuario ha sido creado exitosamente. Contacte a un administrador o instructor para agendar un curso.')
                        return redirect('home')
                except Exception as e:
                    messages.error(request, f'Error al crear el usuario. Error: {e}')
                    return redirect('inscripcion')
        else:
            messages.error(request, 'Error en el formulario. Revise los datos.')
    else:
        form = InscripcionForm()
    return render(request, 'landing/inscripcion.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AlumnoForm, UserForm, InstructorForm, UserInstructorForm, VehiculoForm, PracticaForm, AsignarPracticaForm
from .models import Alumno, Instructor, Vehiculo, Practica, HistorialPractica
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User
from .forms import HistorialPracticaForm


# Vistas para el Panel de Administracion

@login_required
@user_passes_test(lambda u: u.is_staff)  # Solo accesible para usuarios staff (administradores)
def lista_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, 'gestion/lista_alumnos.html', {'alumnos': alumnos})

@login_required
@user_passes_test(lambda u: u.is_staff)
def crear_alumno(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        alumno_form = AlumnoForm(request.POST)
        if user_form.is_valid() and alumno_form.is_valid():
            with transaction.atomic():
                try:
                    username = user_form.cleaned_data['email']
                    if User.objects.filter(username=username).exists():
                        messages.error(request, 'Ya existe un usuario con ese correo electrónico.')
                        return render(request, 'gestion/crear_alumno.html', {'user_form': user_form, 'alumno_form': alumno_form})
                    else:
                        user = User.objects.create_user( #Usamos create user
                            username=username,
                            email=user_form.cleaned_data['email'],
                            password='User123456',
                            first_name=user_form.cleaned_data['first_name'],
                            last_name=user_form.cleaned_data['last_name'],
                        )
                        alumno = alumno_form.save(commit=False)
                        alumno.user = user
                        alumno.save()
                        messages.success(request, 'Alumno creado correctamente.')
                        return redirect('lista_alumnos')
                except Exception as e:
                    messages.error(request, f'Error al crear el usuario. Error: {e}')
                    return render(request, 'gestion/crear_alumno.html', {'user_form': user_form, 'alumno_form': alumno_form})
        else:
            messages.error(request, 'Error al crear el alumno. Revise los datos.')
    else:
        user_form = UserForm()
        alumno_form = AlumnoForm()
    return render(request, 'gestion/crear_alumno.html', {'user_form': user_form, 'alumno_form': alumno_form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    user = alumno.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        alumno_form = AlumnoForm(request.POST, instance=alumno)
        if user_form.is_valid() and alumno_form.is_valid():
            user_form.save()
            alumno_form.save()
            messages.success(request, 'Alumno actualizado correctamente.')
            return redirect('lista_alumnos')
        else:
            messages.error(request, 'Error al actualizar el alumno. Revise los datos.')
    else:
        user_form = UserForm(instance=user)
        alumno_form = AlumnoForm(instance=alumno)
    return render(request, 'gestion/editar_alumno.html', {'user_form': user_form, 'alumno_form': alumno_form, 'alumno': alumno})

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    if request.method == 'POST':
        alumno.user.delete()
        messages.success(request, 'Alumno eliminado correctamente.')
        return redirect('lista_alumnos')
    return render(request, 'gestion/eliminar_alumno.html', {'alumno': alumno})

@login_required
@user_passes_test(lambda u: u.is_staff)
def lista_instructores(request):
    instructores = Instructor.objects.all()
    return render(request, 'gestion/lista_instructores.html', {'instructores': instructores})

@login_required
@user_passes_test(lambda u: u.is_staff)
def crear_instructor(request):
    if request.method == 'POST':
        user_form = UserInstructorForm(request.POST)
        instructor_form = InstructorForm(request.POST)
        if user_form.is_valid() and instructor_form.is_valid():
            with transaction.atomic():
                try:
                    username = user_form.cleaned_data['email']
                    if User.objects.filter(username=username).exists():
                        messages.error(request, 'Ya existe un usuario con ese correo electrónico.')
                        return render(request, 'gestion/crear_instructor.html', {'user_form': user_form, 'instructor_form': instructor_form})
                    else:
                        user = User.objects.create_user(
                            username=username,
                            email=user_form.cleaned_data['email'],
                            password='User123456',
                            first_name=user_form.cleaned_data['first_name'],
                            last_name=user_form.cleaned_data['last_name'],
                        )
                        instructor = instructor_form.save(commit=False)
                        instructor.user = user
                        instructor.save()
                        messages.success(request, 'Instructor creado correctamente.')
                        return redirect('lista_instructores')
                except Exception as e:
                    messages.error(request, f'Error al crear el usuario. Error: {e}')
                    return render(request, 'gestion/crear_instructor.html', {'user_form': user_form, 'instructor_form': instructor_form})

        else:
            messages.error(request, 'Error al crear el instructor. Revise los datos.')
    else:
        user_form = UserInstructorForm()
        instructor_form = InstructorForm()
    return render(request, 'gestion/crear_instructor.html', {'user_form': user_form, 'instructor_form': instructor_form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    user = instructor.user
    if request.method == 'POST':
        user_form = UserInstructorForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Instructor actualizado correctamente.')
            return redirect('lista_instructores')
        else:
            messages.error(request, 'Error al actualizar el instructor. Revise los datos.')
    else:
        user_form = UserInstructorForm(instance=user)
    return render(request, 'gestion/editar_instructor.html', {'user_form': user_form, 'instructor': instructor})

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_instructor(request, instructor_id):
    instructor = get_object_or_404(Instructor, pk=instructor_id)
    if request.method == 'POST':
        instructor.user.delete()
        messages.success(request, 'Instructor eliminado correctamente.')
        return redirect('lista_instructores')
    return render(request, 'gestion/eliminar_instructor.html', {'instructor': instructor})

@login_required
@user_passes_test(lambda u: u.is_staff)
def lista_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'gestion/lista_vehiculos.html', {'vehiculos': vehiculos})

@login_required
@user_passes_test(lambda u: u.is_staff)
def crear_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo creado correctamente.')
            return redirect('lista_vehiculos')
        else:
            messages.error(request, 'Error al crear el vehículo. Revise los datos.')
    else:
        form = VehiculoForm()
    return render(request, 'gestion/crear_vehiculo.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado correctamente.')
            return redirect('lista_vehiculos')
        else:
            messages.error(request, 'Error al actualizar el vehículo. Revise los datos.')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'gestion/editar_vehiculo.html', {'form': form, 'vehiculo': vehiculo})

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado correctamente.')
        return redirect('lista_vehiculos')
    return render(request, 'gestion/eliminar_vehiculo.html', {'vehiculo': vehiculo})

@login_required
@user_passes_test(lambda u: u.is_staff)
def lista_practicas(request):
    practicas = Practica.objects.all()
    return render(request, 'gestion/lista_practicas.html', {'practicas': practicas})

@login_required
@user_passes_test(lambda u: u.is_staff)
def crear_practica(request):
    if request.method == 'POST':
        form = PracticaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Práctica creada correctamente.')
            return redirect('lista_practicas')
        else:
            messages.error(request, 'Error al crear la práctica. Revise los datos.')
    else:
        form = PracticaForm()
    return render(request, 'gestion/crear_practica.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_practica(request, pk):
    try:
        practica = HistorialPractica.objects.get(pk=pk)
        alumno = practica.alumno 
    except HistorialPractica.DoesNotExist:
        messages.error(request, 'Práctica no encontrada.')
        return redirect('lista_alumnos')

    if request.method == 'POST':
        form = HistorialPracticaForm(request.POST, instance=practica)
        if form.is_valid():
            practica_editada = form.save(commit=False)
            if practica_editada.estado == 'realizando' and practica.estado != 'realizando':
                practica_editada.fecha = timezone.now().date()
                practica_editada.hora = timezone.now().time()
            elif practica_editada.estado != 'realizando' and practica.estado == 'realizando':
                practica_editada.fecha = None
                practica_editada.hora = None
                practica_editada.instructor = None
                practica_editada.vehiculo = None
            practica_editada.save()
            messages.success(request, 'Práctica editada correctamente.')
            return redirect('gestion_practicas_alumno', alumno_id=practica.alumno.pk)
        else:
            return render(request, 'gestion/editar_practica.html', {'form': form, 'practica': practica, 'alumno': alumno})
    else:
        form = HistorialPracticaForm(instance=practica)
    return render(request, 'gestion/editar_practica.html', {'form': form, 'practica': practica, 'alumno': alumno})


@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_practica(request, practica_id):
    practica = get_object_or_404(Practica, pk=practica_id)
    if request.method == 'POST':
        practica.delete()
        messages.success(request, 'Práctica eliminada correctamente.')
        return redirect('lista_practicas')
    return render(request, 'gestion/eliminar_practica.html', {'practica': practica})

@login_required
@user_passes_test(lambda u: u.is_staff)
def gestion_practicas_alumno(request):
    practicas = HistorialPractica.objects.all().order_by('alumno', 'practica__tipo')
    return render(request, 'gestion/gestion_practicas_alumno.html', {'practicas': practicas})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_historial_practica(request, historial_practica_id):
    historial_practica = get_object_or_404(HistorialPractica, pk=historial_practica_id)
    instructores = Instructor.objects.all()
    vehiculos = Vehiculo.objects.filter(estado = 'disponible')

    if request.method == 'POST':
        instructor_id = request.POST.get('instructor')
        vehiculo_id = request.POST.get('vehiculo')
        descripcion_resultado = request.POST.get('descripcion_resultado')
        estado = request.POST.get('estado')

        if instructor_id:
            historial_practica.instructor = Instructor.objects.get(pk=instructor_id)
        if vehiculo_id and historial_practica.practica.tipo == 'practica':
            historial_practica.vehiculo = Vehiculo.objects.get(pk=vehiculo_id)

        historial_practica.fecha = timezone.now()
        historial_practica.hora = timezone.now().time()
        historial_practica.descripcion_resultado = descripcion_resultado
        historial_practica.estado = estado
        historial_practica.save()
        messages.success(request, 'Historial de práctica actualizado.')
        return redirect('gestion_practicas_alumno')
    return render(request, 'gestion/editar_historial_practica.html', {'historial_practica': historial_practica, 'instructores': instructores, 'vehiculos':vehiculos})

@login_required
def ver_practicas_alumno(request):
    try:
        alumno = Alumno.objects.get(user=request.user)
        practicas = HistorialPractica.objects.filter(alumno=alumno).order_by('practica__tipo')
        return render(request, 'gestion/ver_practicas_alumno.html', {'practicas': practicas})
    except Alumno.DoesNotExist:
        return render(request, 'gestion/ver_practicas_alumno.html', {'practicas': []})
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_practica_alumno(request, pk):
    practica_alumno = get_object_or_404(HistorialPractica, pk=pk)
    alumno_id = practica_alumno.alumno.pk
    if request.method == 'POST':
        practica_alumno.delete()
        messages.success(request, 'Practica eliminada correctamente.')
        return redirect('gestion_practicas_alumno', alumno_id = alumno_id)
    return render(request, 'gestion/eliminar_practica_alumno.html', {'practica_alumno': practica_alumno})


@login_required
@user_passes_test(lambda u: u.is_staff)
def lista_practicas_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    practicas = HistorialPractica.objects.filter(alumno=alumno).order_by('practica__tipo')
    return render(request, 'gestion/lista_practicas_alumno.html', {'alumno': alumno, 'practicas': practicas})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_practica(request, pk):
    try:
        practica = HistorialPractica.objects.get(pk=pk)
        alumno = practica.alumno  # Obtenemos el alumno ANTES del bloque if request.method
    except HistorialPractica.DoesNotExist:
        messages.error(request, 'Práctica no encontrada.')
        return redirect('lista_alumnos')

    if request.method == 'POST':
        form = HistorialPracticaForm(request.POST, instance=practica)
        if form.is_valid():
            practica_editada = form.save(commit=False)
            if practica_editada.estado == 'realizando' and practica.estado != 'realizando':
                practica_editada.fecha = timezone.now().date()
                practica_editada.hora = timezone.now().time()
            elif practica_editada.estado != 'realizando' and practica.estado == 'realizando':
                practica_editada.fecha = None
                practica_editada.hora = None
                practica_editada.instructor = None
                practica_editada.vehiculo = None
            practica_editada.save()
            messages.success(request, 'Práctica editada correctamente.')
            return redirect('gestion_practicas_alumno', alumno_id=practica.alumno.pk)
        else:
            return render(request, 'gestion/editar_practica.html', {'form': form, 'practica': practica, 'alumno': alumno}) 
    else:
        form = HistorialPracticaForm(instance=practica)
        return render(request, 'gestion/editar_practica.html', {'form': form, 'practica': practica, 'alumno': alumno}) 

@login_required
def lista_practicas_instructor(request):
    try:
        instructor = Instructor.objects.get(user=request.user)
        practicas = HistorialPractica.objects.filter(instructor=instructor).order_by('alumno')
        return render(request, 'gestion/lista_practicas_instructor.html', {'practicas': practicas})
    except Instructor.DoesNotExist:
        return render(request, 'gestion/lista_practicas_instructor.html', {'practicas': []})
    
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def gestion_practicas_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    if request.method == 'POST':
        form = AsignarPracticaForm(request.POST)
        if form.is_valid():
            practicas_a_asignar = form.cleaned_data['practicas']
            for practica in practicas_a_asignar:
                if not HistorialPractica.objects.filter(alumno=alumno, practica=practica).exists():
                    HistorialPractica.objects.create(alumno=alumno, practica=practica, estado='pendiente')
            messages.success(request, 'Prácticas asignadas correctamente.')
            return redirect('gestion_practicas_alumno', alumno_id=alumno_id)
        else:
            messages.error(request, 'Error al asignar las prácticas.')
    else:
        form = AsignarPracticaForm()
    practicas_alumno = HistorialPractica.objects.filter(alumno=alumno)
    return render(request, 'gestion/gestion_practicas_alumno.html', {'alumno': alumno, 'form': form, 'practicas_alumno': practicas_alumno})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_practica_general(request, pk):
    practica = get_object_or_404(Practica, pk=pk)
    if request.method == 'POST':
        form = PracticaForm(request.POST, instance=practica)
        if form.is_valid():
            form.save()
            messages.success(request, 'Práctica editada correctamente.')
            return redirect('lista_practicas')
        else:
            messages.error(request, 'Error al editar la práctica.')
    else:
        form = PracticaForm(instance=practica)
    return render(request, 'gestion/editar_practica_general.html', {'form': form, 'practica': practica})
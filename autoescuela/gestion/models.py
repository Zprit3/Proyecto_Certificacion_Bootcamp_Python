from django.db import models
from django.contrib.auth.models import User

class Alumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_licencia = models.CharField(max_length=10, choices=[('A', 'Clase A'), ('B', 'Clase B'), ('C', 'Clase C')])
    telefono = models.CharField(max_length=20, blank=True, null=True)

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Vehiculo(models.Model):
    modelo = models.CharField(max_length=50)
    patente = models.CharField(max_length=10)
    TIPO_TRANSMISION_CHOICES = [
        ('manual', 'Manual'),
        ('automatico', 'Automático'),
    ]
    tipo_transmision = models.CharField(max_length=20, choices=TIPO_TRANSMISION_CHOICES, default='manual')
    estado = models.CharField(max_length=20, choices=[('disponible', 'Disponible'), ('mantenimiento', 'En Mantenimiento')])
    def __str__(self):
        return f"{self.modelo} ({self.patente})"

class Practica(models.Model):
    tipo = models.CharField(max_length=20, choices=[('teorica', 'Teórica'), ('practica', 'Práctica')])
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre

class HistorialPractica(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    practica = models.ForeignKey(Practica, on_delete=models.CASCADE)
    fecha = models.DateTimeField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    descripcion_resultado = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('realizando', 'Realizando'), ('aprobada', 'Aprobada'), ('reprobada', 'Reprobada')])
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)
    numero_practica = models.AutoField(primary_key = True)
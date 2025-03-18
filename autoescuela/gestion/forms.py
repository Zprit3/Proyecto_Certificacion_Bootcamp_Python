from django import forms
from django.contrib.auth.models import User
from .models import Alumno, Instructor, Vehiculo, Practica, HistorialPractica

class InscripcionForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(max_length=100, label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Correo Electrónico', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(max_length=20, label='Teléfono', widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo_licencia = forms.ChoiceField(choices=Alumno.tipo_licencia.field.choices, label='Tipo de Licencia', widget=forms.Select(attrs={'class': 'form-control'}))

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['tipo_licencia', 'telefono']
        widgets = {
            'tipo_licencia': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = []
        
class UserInstructorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = '__all__'
        widgets = {
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_transmision': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class PracticaForm(forms.ModelForm):
    class Meta:
        model = Practica
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
class HistorialPracticaForm(forms.ModelForm):
    class Meta:
        model = HistorialPractica
        fields = ['instructor', 'fecha', 'hora', 'vehiculo', 'descripcion_resultado', 'estado']
        widgets = {
            'instructor': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'descripcion_resultado': forms.Textarea(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.practica.tipo != 'teorica':
            self.fields['vehiculo'].widget = forms.HiddenInput()
            self.fields['vehiculo'].required = False
        else:
            self.fields['vehiculo'].required = True
        self.fields['instructor'].required = True
        
class AsignarPracticaForm(forms.Form):
    practicas = forms.ModelMultipleChoiceField(
        queryset=Practica.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Prácticas a Asignar",
        required=False,
    )
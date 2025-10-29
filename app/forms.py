# app/forms.py

from django import forms
from .models import Asistencia  # Importamos nuestro modelo


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia

        # 1. Definimos los campos que el usuario SÍ debe llenar
        # Dejamos fuera 'imagen_asistencia' y 'fecha_registro'
        # porque esos se manejarán automáticamente (la cámara y el servidor).
        fields = ['nombre', 'apellido', 'curso', 'materia']

        # 2. (Opcional pero recomendado) Añadimos "widgets"
        # Esto nos permite poner atributos HTML, como placeholders y clases CSS
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ej: Arturo',
                'class': 'form-control',  # Esta clase nos servirá para el estilo
                'required': True
            }),
            'apellido': forms.TextInput(attrs={
                'placeholder': 'Ej: Vera',
                'class': 'form-control',
                'required': True
            }),
            'curso': forms.TextInput(attrs={
                'placeholder': 'Ej: 7mo Semestre "A"',
                'class': 'form-control',
                'required': True
            }),
            'materia': forms.TextInput(attrs={
                'placeholder': 'Ej: Construcción de Software',
                'class': 'form-control',
                'required': True
            }),
        }
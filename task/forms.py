from django import forms
from .models import Task, Predio
from django.core.exceptions import ValidationError
from django.utils import timezone  
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa el titulo'}),
            'description': forms.Textarea(attrs={'class':'form-control','placeholder':'Ingresa la descripccion de la tarea'}),
            'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto mt-2 md-4'}),
        }       

class PredioForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = [
            'proyecto', 
            'vigencia', 
            'gerencia', 
            'categoria_predio_fmi', 
            'estado_folio_matricula', 
            'categoria_fmi', 
            'tipo_documental', 
            'estado', 
            'estado_compra', 
            'sub_estado_compra', 
            'envio_open_text', 
            'accion_tecnica',
            'fecha_solicitud',
            'fecha_respuesta'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={'class': 'form-control'}),
            'vigencia': forms.Select(attrs={'class': 'form-control'}),
            'gerencia': forms.Select(attrs={'class': 'form-control'}),
            'categoria_predio_fmi': forms.Select(attrs={'class': 'form-control'}),
            'estado_folio_matricula': forms.Select(attrs={'class': 'form-control'}),
            'categoria_fmi': forms.Select(attrs={'class': 'form-control'}),
            'tipo_documental': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'estado_compra': forms.Select(attrs={'class': 'form-control'}),
            'sub_estado_compra': forms.Select(attrs={'class': 'form-control'}),
            'envio_open_text': forms.Select(attrs={'class': 'form-control'}),
            'accion_tecnica': forms.Select(attrs={'class': 'form-control'}),
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_respuesta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),

        }
        def clean_fecha_solicitud(self):
            today = timezone.now().date()  # Usamos el método de Django para consistencia
            if self.fecha_solicitud and self.fecha_solicitud > today:
                raise ValidationError('La fecha de solicitud no puede ser posterior a la fecha actual.')
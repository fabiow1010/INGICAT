from django import forms
from .models import Task, Predio
 
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
            'fecha_solicitud': forms.SelectDateWidget(),
            'fecha_respuesta': forms.SelectDateWidget()
        }

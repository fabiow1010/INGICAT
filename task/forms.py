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
        fields = '__all__'
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
            'estrategia': forms.Select(attrs={'class': 'form-control'}),
            'repetido': forms.Select(attrs={'class': 'form-control'}),
            'paquete': forms.Select(attrs={'class': 'form-control'}),
            
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'},format='%Y-%m-%d'),
            'fecha_respuesta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'},format='%Y-%m-%d'),
            'fecha_reiteracion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'},format='%Y-%m-%d'),
            'fecha_pago': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'},format='%Y-%m-%d'),
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_documento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_nueva_busqueda': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'datecompleted': forms.HiddenInput(),
            'ultima_fecha_acceso': forms.HiddenInput(),            
            'campo': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_sig': forms.TextInput(attrs={'class': 'form-control'}),
            'fmi': forms.TextInput(attrs={'class': 'form-control'}),
            'ced_catastral': forms.TextInput(attrs={'class': 'form-control'}),
            'nom_predio': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'entidad': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'documentos_municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_predio_opentext': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_sig_opentext': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_sig_asociado': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable_adquisicion': forms.TextInput(attrs={'class': 'form-control'}),
            'link_sharepoint': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable_seguimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'responsable_nueva_busqueda': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_especificacion': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_pago': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'es_importante': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'adquirir': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }   
    def clean(self):
        cleaned_data = super().clean()
        fecha_solicitud = cleaned_data.get('fecha_solicitud')
        fecha_respuesta = cleaned_data.get('fecha_respuesta')
        if fecha_solicitud and fecha_respuesta:
            if fecha_respuesta < fecha_solicitud:
                self.add_error('fecha_respuesta', 'La fecha de respuesta no puede ser anterior a la de solicitud.')

class PrediosObjetoForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = ['proyecto', 'vigencia', 'gerencia', 'campo', 'cod_sig']
        widgets = {
            'proyecto': forms.Select(attrs={'class': 'form-control'}),
            'vigencia': forms.Select(attrs={'class': 'form-control'}),
            'gerencia': forms.Select(attrs={'class': 'form-control'}),
            'campo': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_sig': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DatosFolioForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = ['categoria_predio_fmi', 'fmi', 'estado_folio_matricula', 'ced_catastral']
        widgets = {
            'categoria_predio_fmi': forms.Select(attrs={'class': 'form-control'}),
            'fmi': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_folio_matricula': forms.Select(attrs={'class': 'form-control'}),
            'ced_catastral': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DatosJuriFMIForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = ['categoria_fmi', 'documento', 'fecha_documento', 'entidad', 'municipio', 'cod_especificacion']
        widgets = {
            'categoria_fmi': forms.Select(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_documento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'entidad': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_especificacion': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ValidacionExistenciaForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = ['nombre_predio_opentext', 'cod_sig_asociado', 'link_sharepoint', 'repetido', 'paquete']
        widgets = {
            'nombre_predio_opentext': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_sig_asociado': forms.TextInput(attrs={'class': 'form-control'}),
            'link_sharepoint': forms.TextInput(attrs={'class': 'form-control'}),
            'repetido': forms.Select(attrs={'class': 'form-control'}),
            'paquete': forms.Select(attrs={'class': 'form-control'}),
        }
        

class EstadoAdquisicionForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = ['estado_compra', 'sub_estado_compra', 'fecha_solicitud', 'fecha_reiteracion',
                  'fecha_respuesta', 'fecha_pago', 'valor_pago', 'fecha_adquisicion',
                  'estrategia', 'responsable_adquisicion']
        widgets = {
            'estado_compra': forms.Select(attrs={'class': 'form-control'}),
            'sub_estado_compra': forms.Select(attrs={'class': 'form-control'}),
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_reiteracion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_respuesta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fecha_pago': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'valor_pago': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'estrategia': forms.Select(attrs={'class': 'form-control'}),
            'responsable_adquisicion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = ['responsable_seguimiento', 'fecha_nueva_busqueda', 'responsable_nueva_busqueda']
        widgets = {
            'responsable_seguimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nueva_busqueda': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'responsable_nueva_busqueda': forms.TextInput(attrs={'class': 'form-control'}),
        }

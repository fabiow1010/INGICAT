from django.contrib import admin
from .models import Task, Predio  


# Configuración para Predio 
class PredioAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'vigencia', 'gerencia', 'estado')  # Campos visibles en la lista
    search_fields = ('proyecto', 'gerencia','user')  # Campos que se pueden buscar
    list_filter = ('vigencia', 'estado')  # Filtros en la barra lateral

# Registrar ambos modelos en el panel de administración

admin.site.register(Predio, PredioAdmin)

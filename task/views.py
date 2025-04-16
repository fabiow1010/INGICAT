from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Predio
from django.db.models import Count, Q
from datetime import date
import matplotlib.pyplot as plt
import io, base64
import pandas as pd
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import (PredioForm,PrediosObjetoForm, DatosFolioForm, DatosJuriFMIForm,
    ValidacionExistenciaForm, EstadoAdquisicionForm, SeguimientoForm)

# Create your views here.

@login_required
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('predios')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


@login_required
def predios(request):
    predios = Predio.objects.filter(user=request.user)
    
    # Obtener parámetros de filtro desde el request
    importancia = request.GET.get('importancia')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    # Filtrar por importancia si está especificado
    if importancia == 'importante':
        predios = predios.filter(es_importante=True)
    elif importancia == 'normal':
        predios = predios.filter(es_importante=False)
    
    # Filtrar por rango de fechas si están especificadas
    if fecha_inicio:
        predios = predios.filter(fecha_solicitud__gte=fecha_inicio)
    if fecha_fin:
        predios = predios.filter(fecha_solicitud__lte=fecha_fin)
    
    context = {"predios": predios}
    return render(request, 'predios.html', context)

@login_required
def predio_completed(request):
    predios = Predio.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'predios.html', {"predios": predios})



@login_required(login_url='signin')
def create_predio(request):
    if request.method == "POST":
        # Crear formularios por secciones
        forms = [
            PrediosObjetoForm(request.POST, prefix='objeto'),
            DatosFolioForm(request.POST, prefix='folio'),
            DatosJuriFMIForm(request.POST, prefix='juri'),
            ValidacionExistenciaForm(request.POST, prefix='validacion'),
            EstadoAdquisicionForm(request.POST, prefix='estado'),
            SeguimientoForm(request.POST, prefix='seguimiento')
        ]

        # Validar si todos los formularios son válidos
        if all(f.is_valid() for f in forms):
            try:
                # Guardar el nuevo predio
                new_predio = forms[0].save(commit=False)  # Usamos el primer formulario para el objeto predio
                new_predio.user = request.user  # Asignamos el usuario
                new_predio.save()  # Guardamos el objeto predio
                
                # Guardamos las demás secciones
                for form in forms:
                    form.instance = new_predio  # Aseguramos que cada formulario esté vinculado al nuevo predio
                    form.save()

                # Mensaje de éxito
                messages.success(request, "Predio creado con éxito.")
                return redirect('predios')  
            except Exception as e:
                # En caso de cualquier error inesperado
                print(e)
                messages.error(request, f"Error al crear el Predio: {str(e)}")
                return redirect('create_predio')  # Redirigir a la misma página si hay error
        else:
            # En caso de que alguno de los formularios no sea válido
            print([form.errors for form in forms])  # Para depurar errores
            messages.error(request, "Formulario inválido. Por favor, revisa los campos.")
            context = {
                "form_objeto": forms[0],  # Mostrar el primer formulario en caso de error
                "form_folio": forms[1],
                "form_juri": forms[2],
                "form_validacion": forms[3],
                "form_estado": forms[4],
                "form_seguimiento": forms[5]
            }
            return render(request, 'create_predio.html', context)
    
    else:
        # Si es GET, inicializamos los formularios vacíos
        forms = [
            PrediosObjetoForm(prefix='objeto'),
            DatosFolioForm(prefix='folio'),
            DatosJuriFMIForm(prefix='juri'),
            ValidacionExistenciaForm(prefix='validacion'),
            EstadoAdquisicionForm(prefix='estado'),
            SeguimientoForm(prefix='seguimiento')
        ]

        context = {
            "form_objeto": forms[0],
            "form_folio": forms[1],
            "form_juri": forms[2],
            "form_validacion": forms[3],
            "form_estado": forms[4],
            "form_seguimiento": forms[5]
        }

        return render(request, 'create_predio.html', context)



def home(request):
    return render(request, 'home.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {
                "form": AuthenticationForm, 
                "error": "Username or password is incorrect."
            })

        login(request, user)
        today = timezone.now().date()
        predios = Predio.objects.filter(user=user)
        for predio in predios:
            if predio.fecha_solicitud:
                predio.ultima_fecha_acceso = today
                predio.actualizar_importancia()
                predio.save()
                print(f"Total predios encontrados para {user.username}: {predios.count()}")
        return redirect('predios')
    


@login_required(login_url='signin')
def predio_detail(request, predio_id):
    predio = get_object_or_404(Predio, pk=predio_id)

    if request.method == 'POST':
        forms = [
            PrediosObjetoForm(request.POST, instance=predio, prefix='objeto'),
            DatosFolioForm(request.POST, instance=predio, prefix='folio'),
            DatosJuriFMIForm(request.POST, instance=predio, prefix='juri'),
            ValidacionExistenciaForm(request.POST, instance=predio, prefix='validacion'),
            EstadoAdquisicionForm(request.POST, instance=predio, prefix='estado'),
            SeguimientoForm(request.POST, instance=predio, prefix='seguimiento')
        ]

        if all(f.is_valid() for f in forms):
            for form in forms:
                form.save()
            return redirect('predios')
        else:
            context = {'error': 'Error al actualizar el predio.'}
    else:
        forms = [
            PrediosObjetoForm(instance=predio, prefix='objeto'),
            DatosFolioForm(instance=predio, prefix='folio'),
            DatosJuriFMIForm(instance=predio, prefix='juri'),
            ValidacionExistenciaForm(instance=predio, prefix='validacion'),
            EstadoAdquisicionForm(instance=predio, prefix='estado'),
            SeguimientoForm(instance=predio, prefix='seguimiento')
        ]
        context = {}

    context.update({
        'predio': predio,
        'form_objeto': forms[0],
        'form_folio': forms[1],
        'form_juri': forms[2],
        'form_validacion': forms[3],
        'form_estado': forms[4],
        'form_seguimiento': forms[5]
    })

    return render(request, 'predio_detail.html', context)


@login_required
def complete_predio(request, predio_id):
    predio = get_object_or_404(Predio, pk=predio_id, user=request.user)
    if request.method == 'POST':
        predio.datecompleted = timezone.now()
        predio.save()
        return redirect('predios')

@login_required
def delete_predio(request, predio_id):
    predio = get_object_or_404(Predio, pk=predio_id, user=request.user)
    if request.method == 'POST':
        predio.delete()
        return redirect('predios')
    return redirect('predio_detail', predio_id=predio_id)
    

def cliente_dashboard(request):
    # Filtros
    campo = request.GET.get('campo', '')
    fmi = request.GET.get('fmi', '')
    proyecto = request.GET.get('proyecto', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    predios = Predio.objects.all()

    if campo:
        predios = predios.filter(campo__icontains=campo)
    if fmi:
        predios = predios.filter(fmi__icontains=fmi)
    if proyecto:
        predios = predios.filter(proyecto=proyecto)
    if fecha_inicio:
        predios = predios.filter(fecha_solicitud__gte=fecha_inicio)
    if fecha_fin:
        predios = predios.filter(fecha_solicitud__lte=fecha_fin)

    # Gráfico de pastel: estado folio matrícula
    estado_counts = (
        predios
        .values('estado_folio_matricula')
        .annotate(total=Count('estado_folio_matricula'))
    )
    labels = [item['estado_folio_matricula'] or 'Sin estado' for item in estado_counts]
    sizes = [item['total'] for item in estado_counts]
    colors = ['#007bff', '#dc3545', '#ffc107', '#28a745', '#6c757d']

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.clf()

    # Gráfico temporal: solicitudes por fecha
    fechas_df = pd.DataFrame(predios.values('fecha_solicitud'))
    fechas_df = fechas_df.dropna()
    fechas_df['fecha_solicitud'] = pd.to_datetime(fechas_df['fecha_solicitud'])
    conteo_fechas = fechas_df['fecha_solicitud'].value_counts().sort_index()

    plt.figure(figsize=(8, 4))
    conteo_fechas.plot(kind='bar', color='#17a2b8')
    plt.title('Solicitudes por Fecha')
    plt.xlabel('Fecha')
    plt.ylabel('Cantidad')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    grafico_fechas = base64.b64encode(buffer2.getvalue()).decode()
    buffer2.close()
    plt.clf()

    # Últimos predios
    ultimos_predios = predios.order_by('-id')[:10]

    context = {
        'graphic': graphic,
        'grafico_fechas': grafico_fechas,
        'ultimos_predios': ultimos_predios,
        'campo': campo,
        'fmi': fmi,
        'proyecto': proyecto,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }

    return render(request, 'dashboard.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Predio
from django.db.models import Count
from datetime import date
import matplotlib.pyplot as plt
import io
import base64


from .forms import PredioForm

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



@login_required
def create_predio(request):
    if request.method == "GET":
        return render(request, 'create_predio.html', {"form": PredioForm()})
    else:
        try:
            form = PredioForm(request.POST)
            new_predio = form.save(commit=False)
            new_predio.user = request.user
            new_predio.save()
            return redirect('predios')
        except ValueError:
            return render(request, 'create_predio.html', {"form": PredioForm(), "error": "Error creando Támite."})




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

    if request.method == 'GET':
        predio_form = PredioForm(instance=predio)
        return render(request, 'predio_detail.html', {'predio': predio, 'predio_form': predio_form})
    
    else:
        try:
            predio_form = PredioForm(request.POST, instance=predio)
            if predio_form.is_valid():
                
                # Guardar el valor original de la fecha_solicitud antes de actualizar
                fecha_solicitud_original = predio.fecha_solicitud  

                predio = predio_form.save(commit=False)  # No guardar aún
                predio.fecha_solicitud = fecha_solicitud_original  # Restaurar el valor original
                
                predio.actualizar_importancia()
                predio.save()  # Guardar finalmente

                return redirect('predios')  
        except ValueError:
            return render(request, 'predio_detail.html', {
                'predio': predio, 
                'predio_form': predio_form, 
                'error': 'Error al actualizar el predio.'
            })


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
    

def cliente_dashboard(request):
    # Obtener datos de la gráfica
    estado_counts = (
        Predio.objects
        .values('estado_folio_matricula')
        .annotate(total=Count('estado_folio_matricula'))
    )

    # Datos para la gráfica
    labels = [item['estado_folio_matricula'] for item in estado_counts]
    sizes = [item['total'] for item in estado_counts]
    colors = ['#007bff', '#dc3545', '#ffc107', '#28a745', '#6c757d']

    # Crear la gráfica con Matplotlib
    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Para que el gráfico se vea como un círculo

    # Guardar la gráfica en un objeto de memoria
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen a base64 para enviarla al template
    graphic = base64.b64encode(image_png).decode('utf-8')

    # Obtener los últimos 10 predios para la tabla
    ultimos_predios = Predio.objects.all().order_by('-id')[:10]

    context = {
        'ultimos_predios': ultimos_predios,
        'graphic': graphic,
    }

    return render(request, 'dashboard.html', context)



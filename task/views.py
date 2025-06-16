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
import io, base64, re
import pandas as pd
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import (
    PredioForm,
    PrediosObjetoForm,
    DatosFolioForm,
    DatosJuriFMIForm,
    ValidacionExistenciaForm,
    EstadoAdquisicionForm,
    SeguimientoForm,
    ConsultaNaturalForm,
)
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import xlsxwriter
from openpyxl import Workbook
from django.http import HttpResponse
from django.db.models import Model
# Create your views here.


@login_required(login_url="signin")
def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect("predios")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Username already exists."},
                )

        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Passwords did not match."},
        )


@login_required(login_url="signin")
def predios(request):
    predios = Predio.objects.all()

    # Obtener parámetros de filtro desde el request
    importancia = request.GET.get("importancia")
    cod_sig = request.GET.get("cod_sig", "")
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    # Filtrar por importancia si está especificado
    if importancia == "importante":
        predios = predios.filter(es_importante=True)
    elif importancia == "normal":
        predios = predios.filter(es_importante=False)

    # Filtrar por rango de fechas si están especificadas
    if fecha_inicio:
        predios = predios.filter(fecha_solicitud__gte=fecha_inicio)
    if fecha_fin:
        predios = predios.filter(fecha_solicitud__lte=fecha_fin)
    # Filtrar por codigo SIG
    if cod_sig:
        predios = predios.filter(cod_sig=cod_sig)

    context = {"predios": predios}
    return render(request, "predios.html", context)


@login_required
def predio_completed(request):
    if request.method == "GET":
        # Filtrar predios completados por el usuario actual
        predios = Predio.objects.filter(datecompleted__isnull=False).order_by(
            "-datecompleted"
        )
        return render(request, "predios.html", {"predios": predios})


@login_required(login_url="signin")
def create_predio(request):
    if request.method == "POST":
        # Crear formularios por secciones
        forms = [
            PrediosObjetoForm(request.POST, prefix="objeto"),
            DatosFolioForm(request.POST, prefix="folio"),
            DatosJuriFMIForm(request.POST, prefix="juri"),
            ValidacionExistenciaForm(request.POST, prefix="validacion"),
            EstadoAdquisicionForm(request.POST, prefix="estado"),
            SeguimientoForm(request.POST, prefix="seguimiento"),
        ]

        # Validar si todos los formularios son válidos
        if all(f.is_valid() for f in forms):
            try:
                # Guardar el nuevo predio
                new_predio = forms[0].save(
                    commit=False
                )  # Usamos el primer formulario para el objeto predio
                new_predio.user = request.user  # Asignamos el usuario
                new_predio.save()  # Guardamos el objeto predio

                # Guardamos las demás secciones
                for form in forms:
                    form.instance = new_predio  # Aseguramos que cada formulario esté vinculado al nuevo predio
                    form.save()

                # Mensaje de éxito
                messages.success(request, "Predio creado con éxito.")
                return redirect("predios")
            except Exception as e:
                # En caso de cualquier error inesperado
                print(e)
                messages.error(request, f"Error al crear el Predio: {str(e)}")
                return redirect(
                    "create_predio"
                )  # Redirigir a la misma página si hay error
        else:
            # En caso de que alguno de los formularios no sea válido
            print([form.errors for form in forms])  # Para depurar errores
            messages.error(
                request, "Formulario inválido. Por favor, revisa los campos."
            )
            context = {
                "form_objeto": forms[
                    0
                ],  # Mostrar el primer formulario en caso de error
                "form_folio": forms[1],
                "form_juri": forms[2],
                "form_validacion": forms[3],
                "form_estado": forms[4],
                "form_seguimiento": forms[5],
            }
            return render(request, "create_predio.html", context)

    else:
        # Si es GET, inicializamos los formularios vacíos
        forms = [
            PrediosObjetoForm(prefix="objeto"),
            DatosFolioForm(prefix="folio"),
            DatosJuriFMIForm(prefix="juri"),
            ValidacionExistenciaForm(prefix="validacion"),
            EstadoAdquisicionForm(prefix="estado"),
            SeguimientoForm(prefix="seguimiento"),
        ]

        context = {
            "form_objeto": forms[0],
            "form_folio": forms[1],
            "form_juri": forms[2],
            "form_validacion": forms[3],
            "form_estado": forms[4],
            "form_seguimiento": forms[5],
        }

        return render(request, "create_predio.html", context)


def home(request):
    return render(request, "home.html")


@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect.",
                },
            )

        login(request, user)
        today = timezone.now().date()
        predios = Predio.objects.filter(user=user)
        for predio in predios:
            if predio.fecha_solicitud:
                predio.ultima_fecha_acceso = today
                predio.save()
                print(
                    f"Total predios encontrados para {user.username}: {predios.count()}"
                )
        return redirect("predios")


@login_required(login_url="signin")
def predio_detail(request, predio_id):
    predio = get_object_or_404(Predio, pk=predio_id)
    puede_editar = (
        request.user.is_superuser
        or request.user.is_staff
        or request.user.groups.filter(name="oficina").exists()
    )

    if request.method == "POST":
        forms = [
            PrediosObjetoForm(request.POST, instance=predio, prefix="objeto"),
            DatosFolioForm(request.POST, instance=predio, prefix="folio"),
            DatosJuriFMIForm(request.POST, instance=predio, prefix="juri"),
            ValidacionExistenciaForm(
                request.POST, instance=predio, prefix="validacion"
            ),
            EstadoAdquisicionForm(request.POST, instance=predio, prefix="estado"),
            SeguimientoForm(request.POST, instance=predio, prefix="seguimiento"),
        ]

        if all(f.is_valid() for f in forms):
            for form in forms:
                form.save()
            return redirect("predios")
        else:
            context = {"error": "Error al actualizar el predio."}
    else:
        forms = [
            PrediosObjetoForm(instance=predio, prefix="objeto"),
            DatosFolioForm(instance=predio, prefix="folio"),
            DatosJuriFMIForm(instance=predio, prefix="juri"),
            ValidacionExistenciaForm(instance=predio, prefix="validacion"),
            EstadoAdquisicionForm(instance=predio, prefix="estado"),
            SeguimientoForm(instance=predio, prefix="seguimiento"),
        ]
        context = {}

    context.update(
        {
            "predio": predio,
            "form_objeto": forms[0],
            "form_folio": forms[1],
            "form_juri": forms[2],
            "form_validacion": forms[3],
            "form_estado": forms[4],
            "form_seguimiento": forms[5],
            "puede_editar": puede_editar,
        }
    )

    return render(request, "predio_detail.html", context)


@login_required
def complete_predio(request, predio_id):
    if request.method == "POST":
        predio = get_object_or_404(Predio, pk=predio_id)
        predio.datecompleted = timezone.now()
        predio.save()
        return redirect("predios")


@login_required
def delete_predio(request, predio_id):
    predio = get_object_or_404(Predio, pk=predio_id)
    if request.method == "POST":
        predio.delete()
        return redirect("predios")
    return redirect("predio_detail", predio_id=predio_id)


@csrf_exempt
def cliente_dashboard(request):
    contexto = {}

    # Filtros GET
    predios = Predio.objects.all()

    # Obtener parámetros de filtro desde el request
    importancia = request.GET.get("importancia")
    cod_sig = request.GET.get("cod_sig", "")
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    # Filtrar por importancia si está especificado
    if importancia == "importante":
        predios = predios.filter(es_importante=True)
    elif importancia == "normal":
        predios = predios.filter(es_importante=False)

    # Filtrar por rango de fechas si están especificadas
    if fecha_inicio:
        predios = predios.filter(fecha_solicitud__gte=fecha_inicio)
    if fecha_fin:
        predios = predios.filter(fecha_solicitud__lte=fecha_fin)
    # Filtrar por codigo SIG
    if cod_sig:
        predios = predios.filter(cod_sig=cod_sig)

    # === GRÁFICO DE PASTEL: Solo estado = "encontrado" ===
    encontrados = predios.filter(estado__iexact="encontrado").count()
    no_encontrados = predios.exclude(estado__iexact="encontrado").count()

    labels_pie = ["Encontrado", "Otros"]
    sizes_pie = [encontrados, no_encontrados]
    colors_pie = ["#d95300", "#6c757d"]

    plt.figure(figsize=(6, 4))
    plt.pie(
        sizes_pie,
        labels=labels_pie,
        colors=colors_pie,
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.axis("equal")
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    graphic = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    plt.clf()

    # === HISTOGRAMA: Conteo por estado ===
    estado_counts = (
        predios.values("estado").annotate(total=Count("id")).order_by("estado")
    )

    estados = [
        item["estado"] if item["estado"] else "Sin estado" for item in estado_counts
    ]
    totales = [item["total"] for item in estado_counts]

    plt.figure(figsize=(6, 4))
    plt.bar(estados, totales, color="#007bff")
    plt.title("Conteo por Estado")
    plt.xlabel("Estado")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format="png")
    grafico_estados = base64.b64encode(buffer2.getvalue()).decode()
    buffer2.close()
    plt.clf()

    # === GRÁFICO TEMPORAL: Solicitudes por fecha ===
    fechas_df = pd.DataFrame(predios.values("fecha_solicitud")).dropna()
    fechas_df["fecha_solicitud"] = pd.to_datetime(fechas_df["fecha_solicitud"])
    fechas_df["solo_fecha"] = fechas_df["fecha_solicitud"].dt.date
    conteo_fechas = fechas_df["solo_fecha"].value_counts().sort_index()

    plt.figure(figsize=(6, 4))
    conteo_fechas.plot(kind="bar", color="#17a2b8")
    plt.title("Solicitudes por Fecha")
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    buffer3 = io.BytesIO()
    plt.savefig(buffer3, format="png")
    grafico_fechas = base64.b64encode(buffer3.getvalue()).decode()
    buffer3.close()
    plt.clf()

    ultimos_predios = predios.order_by("fecha_solicitud")[:10]

    contexto.update(
        {
            "graphic": graphic,
            "grafico_estados": grafico_estados,
            "grafico_fechas": grafico_fechas,
            "ultimos_predios": ultimos_predios,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }
    )

    return render(request, "dashboard.html", contexto)


@login_required(login_url="signin")
def descargar_excel(request):
    if request.method == "POST":
        # Crear el libro de Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte Predios"

        # Obtener todos los campos del modelo Predio
        campos = [f.name for f in Predio._meta.fields if f.related_model != User]

        # Escribir encabezados
        ws.append([campo.replace("_", " ").capitalize() for campo in campos])

        # Consultar los datos
        predios = Predio.objects.all()

        for p in predios:
            fila = []
            for campo in campos:
                valor = getattr(p, campo)

                # Si es una fecha
                if hasattr(valor, 'strftime'):
                    valor = valor.strftime('%Y-%m-%d')
                elif isinstance(valor, Model):  # Omitir otros objetos complejos
                    valor = str(valor)  # O puedes poner valor = '' si no quieres mostrar nada
                fila.append(valor)
            ws.append(fila)

        # Preparar la respuesta
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=reporte_predios.xlsx"
        wb.save(response)
        return response
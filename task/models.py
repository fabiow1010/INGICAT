from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date
from django.utils.timezone import now
from django.utils import timezone
# Create your models here.
class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username

class Predio(models.Model):
    id = models.AutoField(primary_key=True)
    PROYECTO_CHOICES = [('PREDIOS PROPIOS', 'PREDIOS PROPIOS'), ('SERVIDUMBRES', 'SERVIDUMBRES')]
    VIGENCIA_CHOICES = [('2023', '2023'), ('2024', '2024'), ('2025', '2025')]
    GERENCIA_CHOICES = [('VAO', 'VAO'), ('GPA', 'GPA'), ('VRC', 'VRC'), ('GCT', 'GCT'), ('GMA', 'GMA'), ('GRI', 'GRI'), ('GTA', 'GTA'), ('VRO', 'VRO'), ('GCH', 'GCH'), ('GDA', 'GDA'), ('GDT', 'GDT'), ('VPI', 'VPI'), ('VFS', 'VFS')]
    CATEGORIA_PREDIO_FMI_CHOICES = [('COLINDANTE', 'COLINDANTE'), ('FOLIO ESTUDIO', 'FOLIO ESTUDIO'), ('MATRIZ', 'MATRIZ'), ('MATRIZ_COLINDANTE', 'MATRIZ_COLINDANTE'), ('PROPIO', 'PROPIO'), ('SEGREGADO', 'SEGREGADO'), ('SIN INFORMACIÓN', 'SIN INFORMACIÓN')]
    ESTADO_FOLIO_CHOICES = [('ACTIVO', 'ACTIVO'), ('CERRADO', 'CERRADO'), ('SIN INFORMACIÓN', 'SIN INFORMACIÓN')]
    CATEGORIA_FMI_CHOICES = [('ADICIONALES', 'ADICIONALES'), ('COMPLEMENTACIÓN', 'COMPLEMENTACIÓN'), ('SIN INFORMACIÓN', 'SIN INFORMACIÓN'), ('TRADICIÓN', 'TRADICIÓN')]
    TIPO_DOCUMENTAL_CHOICES = [('ACTA', 'ACTA'), ('ACTO ADMINISTRATIVO', 'ACTO ADMINISTRATIVO'), ('AUTO', 'AUTO'), ('CERTIFICADO', 'CERTIFICADO'), ('DECLARACIÓN', 'DECLARACIÓN'), ('DECRETO', 'DECRETO'), ('DEMANDA', 'DEMANDA'), ('DOCUMENTO', 'DOCUMENTO'), ('ESCRITURA', 'ESCRITURA'), ('EXPEDIENTE', 'EXPEDIENTE'), ('RESOLUCIÓN', 'RESOLUCIÓN'), ('SENTENCIA', 'SENTENCIA')]
    ESTADO_CHOICES = [('CARGADO A OTRO PREDIO', 'CARGADO A OTRO PREDIO'), ('CARGADO EN EL PREDIO', 'CARGADO EN EL PREDIO'), ('CARGADO EN SHAREPOINT', 'CARGADO EN SHAREPOINT'), ('NO ENCONTRADO', 'NO ENCONTRADO'), ('NO REQUIERE', 'NO REQUIERE'), ('PENDIENTE VERIFICAR', 'PENDIENTE VERIFICAR'), ('SERVIDOR INGICAT', 'SERVIDOR INGICAT')]
    ESTADO_COMPRA_CHOICES = [('ADQUIRIDO', 'ADQUIRIDO'), ('NO REQUIERE', 'NO REQUIERE'), ('PENDIENTE POR SOLICITAR', 'PENDIENTE POR SOLICITAR'), ('PENDIENTE VERIFICAR', 'PENDIENTE VERIFICAR'), ('SOLICITADO', 'SOLICITADO')]
    SUB_ESTADO_COMPRA_CHOICES = [('ADQUIRIDO PREDIO PROPIOS', 'ADQUIRIDO PREDIO PROPIOS'), ('ADQUIRIDO SERVIDUMBRES', 'ADQUIRIDO SERVIDUMBRES'), ('ERROR REGISTRAL', 'ERROR REGISTRAL'), ('NO APLICA', 'NO APLICA'), ('SOLICITADO / CERTIFICADO NO EXISTE', 'SOLICITADO / CERTIFICADO NO EXISTE'), ('SOLICITADO PREDIO PROPIOS', 'SOLICITADO PREDIO PROPIOS'), ('SOLICITADO SERVIDUMBRES', 'SOLICITADO SERVIDUMBRES')]
    ENVIO_OPEN_TEXT_CHOICES = [('NO', 'NO'), ('NO APLICA', 'NO APLICA'), ('NO REQUIERE', 'NO REQUIERE'), ('PENDIENTE', 'PENDIENTE'), ('SI', 'SI'), ('YA ESTA', 'YA ESTA')]
    ACCION_TECNICA_CHOICES = [('ALIMENTAR EXPEDIENTE PREDIAL', 'ALIMENTAR EXPEDIENTE PREDIAL'), ('ALIMENTAR PREDIO GESTIÓN', 'ALIMENTAR PREDIO GESTIÓN'), ('ALIMENTAR PREDIO MATRIZ', 'ALIMENTAR PREDIO MATRIZ'), ('CARPETA CERO', 'CARPETA CERO'), ('CREAR EXPEDIENTE', 'CREAR EXPEDIENTE'), ('NO REQUIERE', 'NO REQUIERE')]
    REPETIDO_CHOISES =[('REPETIDO','REPETIDO'),('UNICO','UNICO'),('REPETIDO ADQUIRIR','REPETIDO ADQUIRIR'),('NO APLICA','NO APLICA')]
    PAQUETE_CHOISES = [('PAQUETE 4','PAQUETE 4'),('PAQUETE 6','PAQUETE 6'),('SIN PAQUETE','SIN PAQUETE')]
    ESTRATEGIA_CHOISES = [('EMAIL','EMAIL'),('APOYO FISICO','APOYO FISICO'),('NO APLICA','NO APLICA')]

    proyecto = models.CharField(max_length=16, choices=PROYECTO_CHOICES)
    vigencia = models.CharField(max_length=4, choices=VIGENCIA_CHOICES)
    gerencia = models.CharField(max_length=4, choices=GERENCIA_CHOICES)
    categoria_predio_fmi = models.CharField(max_length=100, choices=CATEGORIA_PREDIO_FMI_CHOICES)
    estado_folio_matricula = models.CharField(max_length=100, choices=ESTADO_FOLIO_CHOICES)
    categoria_fmi = models.CharField(max_length=50, choices=CATEGORIA_FMI_CHOICES)
    tipo_documental = models.CharField(max_length=50, choices=TIPO_DOCUMENTAL_CHOICES)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    estado_compra = models.CharField(max_length=50, choices=ESTADO_COMPRA_CHOICES)
    sub_estado_compra = models.CharField(max_length=50, choices=SUB_ESTADO_COMPRA_CHOICES)
    envio_open_text = models.CharField(max_length=50, choices=ENVIO_OPEN_TEXT_CHOICES)
    accion_tecnica = models.CharField(max_length=50, choices=ACCION_TECNICA_CHOICES)
    fecha_solicitud = models.DateField(null=True , blank=True)
    fecha_respuesta = models.DateField(null=True , blank=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    es_importante = models.BooleanField(default=False)
    fecha_reiteracion = models.DateField(null=True, blank=True)
    ultima_fecha_acceso = models.DateField(null=True, blank=True)
    campo=models.CharField(max_length=50, null=True , blank=True)
    cod_sig = models.CharField(max_length=30, null=True , blank=True)
    fmi = models.CharField(max_length=10, default="00000")
    ced_catastral = models.CharField(max_length=31, null=True , blank=True)
    nom_predio = models.CharField(max_length=50, default="Sin Informacion")
    documento = models.CharField(max_length=15, null=True , blank=True)
    fecha_documento= models.DateField(null=True , blank=True)
    entidad = models.CharField(max_length=100, null=True , blank=True)
    municipio = models.CharField(max_length=100,null=True , blank=True)
    documentos_municipio = models.CharField(max_length=150,null=True , blank=True)
    nombre_predio_opentext = models.CharField(max_length=150,null=True , blank=True)
    cod_sig_opentext = models.CharField(max_length=30,null=True , blank=True)
    cod_sig_asociado = models.CharField(max_length=30,null=True , blank=True)
    fecha_pago = models.DateField(null=True , blank=True)
    valor_pago = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    estrategia = models.CharField(max_length=50, choices=ESTRATEGIA_CHOISES, default='NO APLICA')
    responsable_adquisicion = models.CharField(max_length=50,null=True , blank=True)
    link_sharepoint = models.CharField(null=True , blank=True)
    responsable_seguimiento = models.CharField(max_length=50,null=True , blank=True)
    fecha_nueva_busqueda = models.DateField(null=True , blank=True)
    responsable_nueva_busqueda = models.CharField(max_length=50,null=True , blank=True)
    cod_especificacion= models.IntegerField(null=True , blank=True)
    adquirir = models.BooleanField(default=True)
    repetido = models.CharField(max_length=50,choices=REPETIDO_CHOISES, default='NO APLICA')
    paquete = models.CharField(max_length=30, choices=PAQUETE_CHOISES, default='PAQUETE 4')
    
    
    
    
      
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='predios'
    )
    def save(self, *args, **kwargs):
        if not self.ultima_fecha_acceso:
            self.ultima_fecha_acceso = timezone.now().date()

        if self.fecha_solicitud:
            dias_diferencia = (self.ultima_fecha_acceso - self.fecha_solicitud).days
            self.es_importante = dias_diferencia > 8
        else:
            self.es_importante = False

        super().save(*args, **kwargs)  # Llama al método original para guardar

    def __str__(self):
        return f'{self.proyecto} - {self.gerencia} ({self.fecha_solicitud})'
    
    class Meta:
        ordering = ['-fecha_solicitud']
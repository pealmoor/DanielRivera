from django.db import models

# Create your models here.
from django.contrib.auth.models import User

ESTADOS_CITA = [
    ('agendada', 'Agendada'),
    ('cancelada', 'Cancelada'),
    ('reprogramada', 'Reprogramada'),
    ('atendida', 'Atendida'),
]

class Fisioterapeuta(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    especialidad = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()

    def __str__(self):
        return self.usuario.get_full_name()


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion = models.DurationField(help_text="Duración del servicio (ej. 00:30:00 para 30 minutos)")

    def __str__(self):
        return self.nombre


class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fisioterapeuta = models.ForeignKey(Fisioterapeuta, on_delete=models.SET_NULL, null=True, blank=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS_CITA, default='agendada')
    confirmada = models.BooleanField(default=False)

    def __str__(self):
        return f"Cita de {self.paciente} con {self.fisioterapeuta} el {self.fecha} a las {self.hora}"


class NotaCita(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    observaciones = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota de {self.cita}"


class EncuestaSatisfaccion(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE)
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    recomendacion = models.BooleanField()
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Encuesta de {self.cita.paciente} - {self.calificacion}/5"
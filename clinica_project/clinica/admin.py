from django.contrib import admin
from .models import Fisioterapeuta, Paciente, Servicio, Cita, NotaCita, EncuestaSatisfaccion

admin.site.register(Fisioterapeuta)
admin.site.register(Paciente)
admin.site.register(Servicio)
admin.site.register(Cita)
admin.site.register(NotaCita)
admin.site.register(EncuestaSatisfaccion)
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def enviar_recordatorio_cita(cita):
    paciente_email = cita.paciente.usuario.email
    fisioterapeuta_nombre = cita.fisioterapeuta.nombre
    fecha = cita.fecha.strftime('%d/%m/%Y')
    hora = cita.hora.strftime('%H:%M')

    # Construir enlace para confirmar o reprogramar cita
    # Suponemos que tienes URLs para estas vistas con esos nombres
    confirmar_url = settings.DOMAIN + reverse('confirmar_cita', args=[cita.id])
    reprogramar_url = settings.DOMAIN + reverse('reprogramar_cita', args=[cita.id])

    asunto = 'Recordatorio de cita en Clínica Daniel Rivera'
    mensaje = f"""
    Hola {cita.paciente.usuario.get_full_name},

    Le recordamos que tiene una cita agendada para fisioterapia el {fecha} a las {hora} con {fisioterapeuta_nombre}.

    Puede confirmar su asistencia o reprogramar la cita usando los siguientes enlaces:
    Confirmar cita: {confirmar_url}
    Reprogramar cita: {reprogramar_url}

    Gracias por confiar en nosotros.
    """

    send_mail(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        [paciente_email],
        fail_silently=False,
    )

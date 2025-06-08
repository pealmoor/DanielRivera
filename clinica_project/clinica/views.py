from django.shortcuts import render, redirect
from .forms import CitaForm
from .models import Cita, Paciente, Fisioterapeuta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from datetime import date
from .forms import CitaFisioterapeutaForm


@login_required
def agendar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = Paciente.objects.get(usuario=request.user)

            # Asignación automática si no elige fisioterapeuta
            if not cita.fisioterapeuta:
                from .models import Fisioterapeuta
                disponibles = Fisioterapeuta.objects.filter(activo=True)
                for fisio in disponibles:
                    if not Cita.objects.filter(fisioterapeuta=fisio, fecha=cita.fecha, hora=cita.hora).exists():
                        cita.fisioterapeuta = fisio
                        break

            cita.save()

            # Enviar correo
            confirmar_url = request.build_absolute_uri(
                reverse('confirmar_cita', args=[cita.id])
            )
            reprogramar_url = request.build_absolute_uri(
                reverse('reprogramar_cita', args=[cita.id])
            )
            mensaje = f"""
Hola {cita.paciente.usuario.first_name},

Has agendado una cita para el día {cita.fecha} a las {cita.hora} con el fisioterapeuta {cita.fisioterapeuta.nombre}.

Por favor, confirma o reprograma tu cita usando uno de los siguientes enlaces:

✅ Confirmar: {confirmar_url}
🔄 Reprogramar: {reprogramar_url}

Gracias,
Clínica de Fisioterapia Daniel Rivera
            """
            send_mail(
                subject='Confirmación de Cita - Clínica Daniel Rivera',
                message=mensaje,
                from_email=None,
                recipient_list=[request.user.email],
            )

            return redirect('mis_citas')
    else:
        form = CitaForm()
    return render(request, 'clinica/agendar_cita.html', {'form': form})

@login_required
def mis_citas(request):
    paciente = Paciente.objects.get(usuario=request.user)
    citas = Cita.objects.filter(paciente=paciente).order_by('-fecha', '-hora')
    return render(request, 'clinica/mis_citas.html', {'citas': citas})

@login_required
def confirmar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, paciente__usuario=request.user)
    cita.estado = 'confirmada'
    cita.save()
    return HttpResponse("✅ Cita confirmada. Gracias.")

@login_required
def reprogramar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, paciente__usuario=request.user)
    cita.estado = 'reprogramada'
    cita.save()
    return HttpResponse("🔄 Cita marcada como reprogramada. Por favor agenda una nueva desde tu perfil.")

@login_required
def citas_del_dia(request):
    try:
        fisio = Fisioterapeuta.objects.get(usuario=request.user)
    except Fisioterapeuta.DoesNotExist:
        return HttpResponse("No tienes permisos para ver esta sección.")

    citas = Cita.objects.filter(
        fisioterapeuta=fisio,
        fecha=date.today()
    ).order_by('hora')

    return render(request, 'clinica/citas_del_dia.html', {'citas': citas})

@login_required
def detalle_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, fisioterapeuta__usuario=request.user)

    if request.method == 'POST':
        form = CitaFisioterapeutaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            return redirect('citas_del_dia')
    else:
        form = CitaFisioterapeutaForm(instance=cita)

    return render(request, 'clinica/detalle_cita.html', {'form': form, 'cita': cita})

@login_required
def historial_paciente(request, paciente_id):
    # Validar que el usuario sea fisioterapeuta
    try:
        fisio = Fisioterapeuta.objects.get(usuario=request.user)
    except Fisioterapeuta.DoesNotExist:
        return HttpResponse("No tienes permisos para ver esta sección.")

    paciente = get_object_or_404(Paciente, id=paciente_id)
    citas_pasadas = Cita.objects.filter(
        paciente=paciente,
        estado='atendida'  # o puedes incluir estados relevantes
    ).order_by('-fecha')

    return render(request, 'clinica/historial_paciente.html', {
        'paciente': paciente,
        'citas': citas_pasadas,
    })
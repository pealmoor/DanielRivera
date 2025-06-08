from django import forms
from .models import Cita
from datetime import date
from .models import EncuestaSatisfaccion
from django.utils import timezone


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['servicio', 'fecha', 'hora', 'fisioterapeuta']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'min': date.today()}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fisioterapeuta = cleaned_data.get('fisioterapeuta')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if fisioterapeuta and fecha and hora:
            # Verificar si ya hay una cita con este fisioterapeuta en esa fecha/hora
            if Cita.objects.filter(fisioterapeuta=fisioterapeuta, fecha=fecha, hora=hora, estado='agendada').exists():
                raise forms.ValidationError("El fisioterapeuta ya tiene una cita asignada en esa fecha y hora.")

        return cleaned_data
    
class CitaFisioterapeutaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['estado', 'notas']

class EncuestaSatisfaccionForm(forms.ModelForm):
    class Meta:
        model = EncuestaSatisfaccion
        fields = ['calificacion', 'recomendacion', 'comentarios']
        widgets = {
            'calificacion': forms.RadioSelect,
            'comentarios': forms.Textarea(attrs={'rows': 3}),
        }


class ReprogramarCitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora']

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.now().date():
            raise forms.ValidationError("La fecha no puede ser en el pasado.")
        return fecha

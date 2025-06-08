from django import forms
from .models import Cita
from datetime import date


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

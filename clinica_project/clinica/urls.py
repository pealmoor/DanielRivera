from django.urls import path
from . import views

urlpatterns = [
    path('agendar/', views.agendar_cita, name='agendar_cita'),
    path('mis-citas/', views.mis_citas, name='mis_citas'),
    path('confirmar/<int:cita_id>/', views.confirmar_cita, name='confirmar_cita'),
    path('reprogramar/<int:cita_id>/', views.reprogramar_cita, name='reprogramar_cita'),
    path('panel-fisioterapeuta/', views.citas_del_dia, name='citas_del_dia'),
    path('cita/<int:cita_id>/detalle/', views.detalle_cita, name='detalle_cita'),
    path('paciente/<int:paciente_id>/historial/', views.historial_paciente, name='historial_paciente'),
    path('cita/<int:cita_id>/encuesta/', views.encuesta_cita, name='encuesta_cita'),
    path('cita/<int:cita_id>/confirmar/', views.confirmar_cita, name='confirmar_cita'),
    path('cita/<int:cita_id>/reprogramar/', views.reprogramar_cita, name='reprogramar_cita'),





]

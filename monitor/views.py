from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
import os
import shutil
from .models import Camera
from .forms import CameraForm
from .Interfaz import Interfaz
import requests,json
from requests.auth import HTTPDigestAuth

# Create your views here.

class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
    
class HomePageView(TemplateView):
    """Clase que renderiza el index del sistema"""
    template_name = 'home.html'
    
class CameraListView(ListView):
    model = Camera
    
    def get_queryset(self):
        # usuario = self.request.user
        camera=Camera.objects.all()
        # print("Usuario y cliente: ", usuario, camera)
        return camera

class CameraDetailView(DetailView):
    model = Camera

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ### ------------------------------- Declarar la interfaz
        interfaz_api = Interfaz()
        print("#-------------------Prueba Camara: ")
        body = ""
        interfaz_api.establecer_protocol('http')
        interfaz_api.establecer_server('elipgomexico.ddns.net:1938')
        interfaz_api.establecer_abs_path('cgi-bin')
        interfaz_api.establecer_auth(HTTPDigestAuth('test', 'test$2022'))
        interfaz_api.establecer_metodo('GET')
        #interfaz_api.establecer_encabezado({'Content-Type': 'application/json'})

        """ Obtener informacion general """
        interfaz_api.establecer_query('configManager.cgi?action=getConfig&name=General')
        general = interfaz_api.enviar(Interfaz.PROCESO,body)

        """ Obtener hora actual"""
        interfaz_api.establecer_query('global.cgi?action=getCurrentTime')
        current_time = interfaz_api.enviar(Interfaz.PROCESO,body)

        """ Obtener locales"""
        interfaz_api.establecer_query('configManager.cgi?action=getConfig&name=Locales')
        locales = interfaz_api.enviar(Interfaz.PROCESO,body)

        """ Obtener tipo"""
        interfaz_api.establecer_query('magicBox.cgi?action=getDeviceType')
        device_type = interfaz_api.enviar(Interfaz.PROCESO,body)

        """ Obtener nombre de maquina"""
        interfaz_api.establecer_query('magicBox.cgi?action=getMachineName')
        machine_name = interfaz_api.enviar(Interfaz.PROCESO,body)

        """ Obtener snapshot"""
        interfaz_api.establecer_query('snapshot.cgi?channel=1')
        snapshot = interfaz_api.enviar(Interfaz.PROCESO,body)
        with open("monitor/static/monitor/snapshot.jpg", 'wb') as f:
            snapshot.raw.decode_content = True
            shutil.copyfileobj(snapshot.raw, f)  

        """
        file = open("monitor/static/monitor/snapshot.jpg", "w")
        file.write(snapshot.text)
        file.close()"""
        

        context['general']=general.text
        context['current_time']=current_time.text
        context['locales']=locales.text
        context['device_type']=device_type.text
        context['machine_name']=machine_name.text
        context['snapshot']=snapshot.text

        return context

class CameraCreateView(CreateView):
    model = Camera
    form_class = CameraForm
    success_url = reverse_lazy('camera:cameras')

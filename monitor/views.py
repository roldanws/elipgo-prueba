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
import requests,json
from requests.auth import HTTPDigestAuth

from monitor.Monitor.Interfaz import Interfaz
from monitor.Monitor.Comunicacion import Comunicacion
from monitor.Monitor.Variable import Variable
from monitor.Monitor.Camera import Camera as Cam


# Create your views here.
class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
    

    
class CameraDetailView(DetailView):
    """ Vista encargada de detallar el dispositivo seleccionado """
    model = Camera
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ###-----Nueva estructura
        puerto = Interfaz("api")
        puerto.modificarConfiguracion(
                                    dispositivo = Interfaz.CAMARA_DAHUA, 
                                    protocolo = 'http', 
                                    servidor = 'elipgomexico.ddns.net', 
                                    puerto = '1938', 
                                    usuario = 'test', 
                                    password = 'test$2022'
                                    )
        comunicacion = Comunicacion ()
        puerto.inicializar()
        
        # Se crea y se configura el dispositivo
        camera1 = Cam("Camera 1", "CAM-001", "En camara")
        camera1.establecerPuerto(puerto)
        camera1.establecerComunicacion (comunicacion)
        
        general = camera1.obtener_datos_generales()
        current_time = camera1.obtener_current_time()
        locales = camera1.obtener_locales_config()
        device_type = camera1.obtener_device_type()
        machine_name = camera1.obtener_machine_name()
        
        camera1.actualizar_motion_settings(estado="true")
        motion_settings = camera1.obtener_motion_settings()

        snapshot = camera1.obtener_snapshot()
        with open("monitor/static/monitor/snapshot.jpg", 'wb') as f:
            snapshot.raw.decode_content = True
            shutil.copyfileobj(snapshot.raw, f)  


        context['general']=general
        context['current_time']=current_time
        context['locales']=locales
        context['device_type']=device_type
        context['machine_name']=machine_name.text
        context['motion_settings']=motion_settings
        return context


class CameraListView(ListView):
    """ Vista encargada de listar los dispositivos registrados """
    model = Camera
    def get_queryset(self):
        camera=Camera.objects.all()
        return camera

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cameras = []
        for camera in self.object_list:
            
            puerto = Interfaz("api {}".format(camera.usuario))
            puerto.modificarConfiguracion(
                                    dispositivo = Interfaz.CAMARA_DAHUA, 
                                    protocolo = 'http', 
                                    servidor = camera.ip, 
                                    puerto = camera.puerto, 
                                    usuario = camera.usuario, 
                                    password = camera.password,
                                    )
            comunicacion = Comunicacion ()
            puerto.inicializar()
            cam = Cam("Camera 1", "CAM-{}".format(camera.id), "En camara")
            cam.establecerPuerto(puerto)
            cam.establecerComunicacion (comunicacion)
            if cam.obtener_serial_no():
                #print("sn",cam.obtener_serial_no())
                serial_no = cam.variables[2].obtenerDescripcion()
                cameras.append(serial_no)
                camera.serial_no = serial_no
                camera.save()
            else:
                camera.serial_no = '0'
                camera.save()

        context['cameras_serial_no']=cameras
        return context

        '''puerto = Interfaz("api")
        puerto.modificarConfiguracion(
                                    dispositivo = Interfaz.CAMARA_DAHUA, 
                                    protocolo = 'http', 
                                    servidor = 'elipgomexico.ddns.net', 
                                    puerto = '1938', 
                                    usuario = 'test', 
                                    password = 'test$2022'
                                    )
        comunicacion = Comunicacion ()
        puerto.inicializar()
        
        # Se crea y se configura el dispositivo
        camera1 = Cam("Camera 1", "CAM-001", "En camara")
        camera1.establecerPuerto(puerto)
        camera1.establecerComunicacion (comunicacion)
        '''


        '''interfaz = Interfaz()
        body = ""
        print("con:::",context['camera_list'][0].ip, context['camera_list'][0].puerto)
        interfaz.establecer_protocol('http')
        interfaz.establecer_server('{}:{}'.format(context['camera_list'][0].ip,context['camera_list'][0].puerto))
        interfaz.establecer_metodo('GET')
        interfaz.establecer_auth(HTTPDigestAuth('test', 'test$2022'))

        """ Obtener flujo de video"""
        interfaz.establecer_ruta('cgi-bin/cgi-bin/magicBox.cgi?action=getSerialNo')
        serial_no = interfaz.enviar(Interfaz.PROCESO,body)
        context['serial_no']=serial_no.text

        """ Suscribir a evento Motion"""
        interfaz.establecer_ruta('cgi-bin/snapManager.cgi?action=attachFileProc&Flags[0]=Event&Events=[VideoMotion]&heartbeat=5')
        r = interfaz.enviar(Interfaz.PROCESO,body)
        print("Sucrubeee",r.text)
        context['r']=r.text
        return context'''


class CameraCreateView(CreateView):
    model = Camera
    form_class = CameraForm
    success_url = reverse_lazy('camera:cameras')

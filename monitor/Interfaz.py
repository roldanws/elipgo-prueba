# Create your tests here.
from datetime import datetime, date, time, timedelta
import os,sys,time
import requests,json
from requests.auth import HTTPDigestAuth



class Interfaz:
    """
    Clase utulizada para consumir un api con python 
    """
    ADMINISTRACION = 1
    PROCESO = 2
    INTERFAZ = 3
    CODIGOS_EXITOSOS = (200,201,206)
    def __init__(self):
        self.url = ""
        self.auth = ""
        self.encabezado = ""
        self.metodo = ""
        self.datos = ""
        self.protocol = ""
        self.server = ""
        self.abs_path = ""
        self.query = ""
        self.status_code = ""
        self.response = ""
        self.lista_de_variables = ""


    def obtener_url(self,url):
        return self.url
    def obtener_encabezado(self,encabezado):
        return self.encabezado
    def obtener_metodo(self,metodo):
        return self.metodo

    def construir_url(self):
        self.url =  "{}://{}/{}/{}".format(self.protocol,self.server,self.abs_path,self.query)
    def establecer_protocol(self,protocol):
        self.protocol = protocol
    def establecer_server(self,server):
        self.server = server
    def establecer_abs_path(self,abs_path):
        self.abs_path = abs_path
    def establecer_query(self,query):
        self.query = query

    def establecer_auth(self,auth):
        self.auth = auth
    def establecer_encabezado(self,encabezado):
        self.encabezado = encabezado
    def establecer_metodo(self,metodo):
        self.metodo = metodo

    def establecer_lista_de_variables(self,lista_de_variables):
        self.lista_de_variables = lista_de_variables
        
    def establecer_encabezados(self,encabezados):
        self.modo_operacion = modo_operacion
        
    def enviar(self,tipo = 0, *args, **kargs):
        err = 0
        for item in args:
            #print (item)
            #for i, it in enumerate(item):
            #    print(i,it)
        
                
            if self.validar_datos(item):
                self.datos = item
            else:
                self.response =  {"error":"datos invalidos"}

        try:
            if self.metodo == 'GET':
                self.construir_url()
                response = requests.get(
                self.url,
                auth=self.auth,
                headers=self.encabezado,
                verify=False,  #Necesario para Diguest auth
                stream=True
                )
                if response.status_code not in self.CODIGOS_EXITOSOS:
                    err = 1
                else:
                    return response
                
            elif self.metodo == 'POST':
                #print("metodo POST: ",self.metodo)
                response = requests.post(
                self.url, data=json.dumps(self.datos),
                headers=self.encabezado
                )
                if response.status_code not in self.CODIGOS_EXITOSOS:
                    err = 1
                
                
            elif self.metodo == 'PUT':
                pass
            elif self.metodo == 'DELETE':
                pass

            self.status_code = response.status_code
            self.response = response.json()

            if err:
                print("Ocurrio un error:",response.status_code)
            else: 
                return self.response
        except:
            self.response = 0
            text = "[{}] [Error3] Vista sin respuesta".format(time.strftime("%Y-%m-%d %H:%M:%S"))
            #print(colored(text, 'red'))
            print(text)

    
    def validar_datos(self,datos):
        if datos:
            return 1
        else: 
            return 0



    

def main():
    
    ### ------------------------------- Declarar la interfaz
    interfaz_api = Interfaz()
    print("#-------------------Prueba Camara: ")
    body = ""
    #metodo = "GET"
    interfaz_api.establecer_protocol('http')
    interfaz_api.establecer_server('elipgomexico.ddns.net:1938')
    interfaz_api.establecer_abs_path('cgi-bin')
    interfaz_api.construir_url()
    interfaz_api.establecer_metodo('GET')
    interfaz_api.establecer_auth(HTTPDigestAuth('test', 'test$2022'))
    #interfaz_api.establecer_encabezado({'Content-Type': 'application/json'})
    interfaz_api.establecer_query('configManager.cgi?action=getConfig&name=General')
    interfaz_api.establecer_query('snapshot.cgi?channel=1')
    response = interfaz_api.enviar(Interfaz.PROCESO,body)
    print(response.text)
    
if __name__ == "__main__":
    main()


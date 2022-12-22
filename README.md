# elipgo-prueba

En la url http://127.0.0.1:8000/ es una vista para agregar 1 o mas camaras

- Cuenta con un boton para agregar una camara ingresando la url y su autenticacion

- El boton de Ver enviara a la url http://127.0.0.1:8000/camera/1 donde se accede a la camara
    y se consultan algunos metodos del api

- Tambien se toma en ese momento un snapshot, se manda a un archivo .jpg y se muestra en la vista

- El archivo monitor/Interfaz.py es el encargado de hacer la comunicacion con el Api con la libreria requests

Por agregar:
Se agregaran botones para tomar un snapshoot
Por medio del api nos suscribiriemos al evento de deteccion de movimiento y almacenare las imagenes en una galeria



[ Ejecucion ]

pip install -r requeriments
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# Información sobre el reto
El reto consiste en sobrepasar (bypass) una subida de archivos, el servidor permite la subida de archivos a este pero tiene un filtro para sólo permitir
archivos de tipo imagen según la extensión del archivo (jpg, png...), sin embargo, el filtro está mal diseñado, de forma que si se añaden una primera extensión
válida y luego la extensión .php, al ser accedido el archivo en el servidor, el servidor pensará que este archivo es php y ejecutará el código que contiene.

El archivo aportado por el CTF "readFlag.php" debe ser usado para leer la flag que se encuentra en la raíz del contenedor, también se podría subir cualquier otro
código php, lo que incluye poder ejecutar una shell inversa y navegar desde esta shell a la raíz para leer la flag.

Por lo tanto solucionar el reto es tan fácil como darse cuenta de que el servidor sólo comprueba la primera extensión del archivo y renombrar el archivo php que se 
quiera subir a "nombre.png.php" o cualquier otra extensión permitida en vez de "png", después habría que acceder a este archivo en la carpeta uploads/, es decir:

http://"ip del servidor":"puerto"/uploads/"nombre.png.php"

### Dockerfile
Contiene los comandos para crear la imagen de Docker.

### apacheFiles/
Contiene los archivos que se deben copiar en la carpeta del servidor, los que permiten la subida de archivos y la carpeta en la que se subirán las "imágenes".

### startServer.sh
Script para crear la imagen de docker a través del Dockerfile y crear el contenedor correspondiente.

### readFlag.php
Es el archivo con el código php que los participantes deben subir para conseguir la flag, otra opción sería que subiesen una shell inversa que les diese 
acceso al sistema y desde ahí navegar hasta la raíz del sistema de archivos para leer la flag.

### flag.txt
La propia flag del reto, se copia a la raíz del sistema de archivos del contenedor.

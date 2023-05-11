# Embedded Nano: Writeup

> Me han pasado esta foto tan rara de Fernando Alonso. ¿Alguien sabe qué quiere decir?

>_Dificultad: Media_

En este reto nos proporcionan una foto curiosa de Fernando Alonso. Por el nombre del reto (Embedded Nano) y la categoría en la que se encuentra, esteganografia (proceso de ocultar información dentro de otro archivo o mensaje sin que sea detectado), lo lógico es busgar 'algo' dentro de esta imagen. Existen muchas herramientas dedicadas a esta categoría como Steghide, OpenStego, Steganography Studio, etc... 
En mi caso, voy a usar `Steghide`.

Para extraer archivos embebidos se usa el siguiente comando:
```sh
$ steghide extract -sf nano.jpg
```

Esto nos va a pedir un _passphrase_. Muchas veces basta con pulsar `Enter` ya que muchas veces no se emplean _passphrase_ necesariamente. En este caso vemos que sí que se ha usado, ya que nos deniega el acceso al no insertar el correcto. 
Llegados a este punto es previsible pensar que la contraseña debe de estar escondida en algún sitio. Podemos ver qué muestran los metadatos de la imageen. Para ello usamos la herramienta `Exiftool`, la cual nos permite leer, escribir y editar los metadatos de archivos. 

```sh
$ exiftool nano.jpg
```

Esto nos devuelve los siguientes metadatos:
```sh
ExifTool Version Number         : 11.88
File Name                       : nano.jpg
Directory                       : .
File Size                       : 2.1 MB
File Modification Date/Time     : 2023:05:09 18:45:33+02:00
File Access Date/Time           : 2023:05:10 18:00:26+02:00
File Inode Change Date/Time     : 2023:05:10 18:00:17+02:00
File Permissions                : rwxrwxrwx
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Current IPTC Digest             : 10dbd39e38d2b070b4f367b51aedb831
Copyright Notice                : ©2023 Fernando Alonso, all rights reserved
Application Record Version      : 4
XMP Toolkit                     : Image::ExifTool 11.88
Creator                         : Passwd:elgatitoblanco123
Rights                          : ©2023 Fernando Alonso, all rights reserved
Image Width                     : 4000
Image Height                    : 2966
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:4:4 (1 1)
Image Size                      : 4000x2966
Megapixels                      : 11.9
```
Si los leemos, en el tag de Creator aparece `Passwd:elgatitoblanco123`. Probamos esto como passphrase y efectivamente se trata de la contraseña correcta.

Hecho esto habremos extraído un zip llamado `hiddenData.zip`. Lo descomprimimos:

```sh
$ unzip -d hiddenData hiddenData.zip
```
Y esto nos descomprime otro zip `flag.zip` y un archivo de texto `credentials.txt`.
Si volvemos a hacer unzip de `flag.zip` veremos que nos pide una contraseña para ello, está protegido. Por lo que necesitaremos encontrar la contraseña correspondiente en el archivo `credentials.txt`. En este archivo hay 300 contraseñas, por lo que hacerlo a mano no es una opción (o sí). 
Necesitaremos usar brute force (método de ataque que usa la fuerza bruta, es decir, prueba todas las combinaciones posibles hasta encontrar la correcta).
Las podibilidades para hacer brute force son muchas, yo usaré el siguiente repositorio de GitHub para crackear zip con Python3: [Python3 Zip Cracker](https://github.com/jvasquez21/Python3-Zip-Password-Cracking). 
De este repositorio nos descargaremos el [zip-cracker.py](https://raw.githubusercontent.com/jvasquez21/Python3-Zip-Password-Cracking/master/zip-cracker.py) y modificaremos la línea:

```py
dictionary_attack = "rockyou.txt"
```
Y en vez de seleccionar el diccionario del rockyou.txt, pondremos `credentials.txt`. 

Y ya lo único que faltaría sería ejecutarlo:

```sh
$ python3 zip-cracker.py flag.zip
```

```sh
$ cat flag.txt
$ ETSIIT_CTF{StegAn0gRAphY_Is_S0_FuN}
```
Y ya tendríamos la flag
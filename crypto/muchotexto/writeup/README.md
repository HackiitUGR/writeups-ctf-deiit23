# Writeup del reto: "Mucho texto"

En este reto nos dan un archivo en formato .txt y nos dicen que se encuentra alterado, con muchos caracteres sin sentido alguno.

Si lo descargamos y abrimos, vemos que se trata efectivamente de un archivo muy largo. Está claro que está codificado de alguna manera, si no vemos de qué 
codificación se trata, podemos usar alguna herramienta online para detectar la codificación como: [CyberChef](https://gchq.github.io/CyberChef/) o [DenCode](https://dencode.com/). En este caso, es fácil determinar que se trata de codificación en Base64, por el conjunto de caracteres que se emplea (rango de A-Z, a-z y 0-9) y además, si observamos el final del archivo, este acaba con el símbolo "=", el cual es usado como sufijo especial en Base64.

## Decodificamos 🔧

Una vez sabemos que se trata de Base64, podremos decodificar el texto. Al ser un archivo tan grande, es recomendable que lo hagamos usando herramientas de nuestro propio sistema, ya que si intentamos decodificarlo con herramientas online muy probablemente nos de error.
En este caso vamos a decodificarlo con _python_.
Esto lo hacemos  con las funciones _base64.b64decode()_ y _decode("utf-8")_. Con la primera decodificaremos la cadena de texto pasada como argumento y nos devolverá la secuencia de bytes que representan la información original antes de que se codificase en Base64. Y con la segunda decodificaremoslos bytes en formato UTF-8 para devolver la cadena de texto original que había sido codificada en Base64.

```py
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode("utf-8")
```
Si hacemos esto, vemos que se vuelve a obtener una cadena muy larga de texto de nuevo en Base64. Esto lo podemos repetir varias veces obteniendo cada vez una cadena más pequeña. Concretamente 33 veces son las que necesitaríamos realizar este mismo proceso para obtener la flag.
```
    Flag: ETSIIT_CTF{33__times__Base64_COM0__33?_EL_NANO?}
```

### Optimización 

Una forma más eficiente de hacerlo (y la que esperamos que hayáis hecho, por vuestro bien mental) una vez nos damos cuenta de que siempre que decodificamos obtenemos Base64, es automatizar el proceso hasta que se encuentra con un string decodificado que empiece con el formato de la flag "ETSIIT_CTF". Esto lo podemos hacer de manera muy sencilla con python tal que:

```py
import base64

encoded_string = input(" ")
decoded_string = ""

while not decoded_string.startswith("ETSIIT_CTF"):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode("utf-8")
    encoded_string = decoded_string

print("Flag:", decoded_string)
```
De esta forma tardaremos muy poco en encontrar la flag, bastará con llamar al programa y pasarle como argumento el archivo.txt.

```
$ python3 CTF_decryptBase64.py < archivo.txt

 Flag: ETSIIT_CTF{33__times__Base64_COM0__33?_EL_NANO?}
```

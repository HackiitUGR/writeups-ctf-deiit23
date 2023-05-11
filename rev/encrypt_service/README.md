# Encrypt Service Writeup
### Descripción
Mediante un análisis forense hemos sido capaz de recuperar dos archivos. Uno de ellos parece ser un mensaje cifrado, y el otro creemos que tiene que ver con cómo se cifró el mensaje. Serás capaz de recuperar el mensaje original?

Dificultad: media.

### Writeup
En este reto se nos proporciona un archivo `msg.enc` que debemos descifrar. Inspeccionándolo parece ser base64. Decodificándolo parece que es una serie de bytes seguidos de un número decimal.

```
$ cat msg.enc
3MoRVg74t2RmiocyCEsB+4CuTizFjF4mTUOrWL3FFmdEtJpgMTY4MjYwMTIwMi41MDg4Njg=
$ cat msg.enc | base64 -d | xxd
00000000: dcca 1156 0ef8 b764 668a 8732 084b 01fb  ...V...df..2.K..
00000010: 80ae 4e2c c58c 5e26 4d43 ab58 bdc5 1667  ..N,..^&MC.X...g
00000020: 44b4 9a60 3136 3832 3630 3132 3032 2e35  D..`1682601202.5
00000030: 3038 3836 38                             08868
```

También se nos proporciona un fichero `chall.pyc`. La orden `file` nos dice que se trata de un archivo compilado de python3.8, y parece que no podremos ejecutarlo a no ser que tengamos esa misma versión de python.

```
$ file chall.pyc
chall.pyc: python 3.8 byte-compiled
$ python3 chall.pyc
RuntimeError: Bad magic number in .pyc file
```

El objetivo es decompilar el archivo `chall.pyc` para obtener el código fuente original. Una búsqueda en google del estilo de "python decompile pyc" nos lleva a algunos proyectos como `decompyle3` o `uncompyle6`. Probamos con [`decompyle3`](https://github.com/rocky/python-decompile3). Instalándolo con `pip install decompyle3` y ejecutando `decompyle3 chall.pyc` obtenemos el código fuente original, que ya podremos ejecutar de forma normal:

```py
import hashlib, os, random, base64
from datetime import datetime

def encrypt(msg):
    t = datetime.now().timestamp()
    random.seed(t)
    result = bytearray()
    for b in msg:
        result.append(b ^ random.randint(0, 255))
    else:
        result += str(t).encode()
        return base64.b64encode(result).decode()


def main():
    passwd = input('Introduce la contraseña: ')
    if hashlib.md5(passwd.encode()).hexdigest() != 'e1568c571e684e0fb1724da85d215dc0':
        print('Wrong!')
        return
    print('Bienvenido al servicio de cifrado.')
    passwd = input('Introduce el mensaje: ')
    print(encrypt(passwd.encode()))


if __name__ == '__main__':
    main()
```

Vemos que el programa inicialmente nos pide una contraseña. Podemos introducir el hash en [crackstation](https://crackstation.net/) para obtener que la contraseña es `l33t`, o ya que disponemos del código fuente, podemos simplemente comentar esas líneas.

A continuación nos pide un mensaje, lo cifra, e imprime el resultado. Suponemos que así es como se ha cifrado el archivo `msg.enc`, y el objetivo es hacer una función de descifrado. Veamos la función `encrypt()`:

```py
def encrypt(msg):
    t = datetime.now().timestamp()
    random.seed(t)
    result = bytearray()
    for b in msg:
        result.append(b ^ random.randint(0, 255))
    else:
        result += str(t).encode()
        return base64.b64encode(result).decode()
```

Comienza obteniendo una timestamp del instante de tiempo actual, y usándola como semilla para `random`. A continuación, por cada byte del mensaje, añade al resultado dicho byte xoreado con un byte generado aleatoriamente con `random`. Finalmente (cláusula `else` del `for`), añade al resultado la timestamp usada como semilla, y codifica el resultado con base64.

Ya que los números aleatorios dependen de la semilla, y esta cambia cada vez, dos cifrados de un mismo mensaje serán siempre diferentes. Además, no se podrá recuperar el mensaje original sin la semilla que se usó para cifrarlo, ya que los bytes aleatorios usados para cifrar con xor no serán los mismos. Afortunadamente, el resultado incluye al final la timestamp usada como semilla.

Por tanto, para descifrar `msg.enc` es necesario:
1. Decodificar con base64.
2. Obtener la timestamp del final del mensaje y usarla como semilla. De esta forma, generaremos los mismos bytes aleatorios que se usaron cuando se cifró el mensaje.
3. Aplicar el cifrado xor al resto del mensaje. Ya que xor es una operación simétrica y estamos generando los mismos bytes, esto producirá el mensaje original.

En python:

```py
def decrypt(msg):
	msg = base64.b64decode(msg)
	t = float(msg[-17:].decode())
	random.seed(t)

	result = bytearray()
	for b in msg[:-17]:
		result.append(b ^ random.randint(0, 0xFF))
	return result.decode()

def main():
	with open("msg.enc") as f:
		msg_enc = f.read()
	print(decrypt(msg_enc))
```

Ejecutando el script obtenemos la flag:
```
$ python3 solve.py
ETSIIT_CTF{pyc_revers3_engin33r1ng!}
```

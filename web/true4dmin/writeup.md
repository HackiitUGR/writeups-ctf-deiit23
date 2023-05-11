# Writeup True4dmin

Este servidor web tiene un mecanísmo de registro e inicio de sesión.
Si nos creamos una cuenta de forma corriente, veremos que al iniciar sesión nos dice que no somos administradores.

Si inspeccionamos las peticiones que se hacen a la hora del registro, podremos apreciar un valor oculto, que se llama admin y tiene el valor `cfcd208495d565ef66e7dff9f98764da`. Este valor es `0` en MD5, por lo que calcularemos `1` en MD5.

`MD5(1) = c4ca4238a0b923820dcc509a6f75849b`

Ahora modificaremos el valor y haremos la petición POST del registro.

Cuando iniciemos sesión con el usuario que modificamos el registro podremos ver la flag.
`ETSIIT_CTF{Y0U_B3C4M3_4N_4DM1N}`

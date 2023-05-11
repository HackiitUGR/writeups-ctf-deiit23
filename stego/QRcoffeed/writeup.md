# QR disaster: Write-up

> Oh no! Se me ha caído el café en este QR. Tiene información muy importante,
> ¿puedes recuperarlo por mi?

<img src="https://i.imgur.com/3PnC40A.png" alt="drawing" width="400"/>

El objetivo del reto es bastante obvio: reparar el código QR. Para ello,
sacamos la herramienta más importante del cinturón del hacker: 
GIMP/paint.

Hay otro tipo de herramientas para editar imágenes pixeladas (hay gente 
que lo hace en Excel), pero si no tienes ninguna, puedes escalar la
imagen hasta que un "cuadrado" del QR esté contenido en un pixel.

Primero limpiamos los tres cuadrados grandes de las esquinas, que
sirven para saber la orientación del QR al dispositivo que lee.
Después los cuadrados pequeños 3x3 del centro (llamados marcas de 
alineamiento) y el marco de píxeles blancos exterior (zona silenciosa). 
Finalmente, nos queda una línea de un píxel manchada.

<img src="https://i.imgur.com/x815Dn3.png" alt="drawing" width="400"/>

Ahora, la gran mayoría de lectores de códigos QR pueden leer la
información que hay dentro. Si aún no puedes, pinta el *timing pattern*
en la parte manchada, que consiste en píxeles blancos y negros alternos.
[Aquí se explica de manera más visual las partes de un código QR.](https://epochonline.com/Blog/ArtMID/945/ArticleID/34/The-parts-of-a-QR-Code)
La imagen limpia del todo:

<img src="https://i.imgur.com/gkc77TV.png" alt="drawing" width="400"/>


Si se escanea, verás este link: https://imgur.com/a/H5ipWAS. Te lleva
a una imagen parecida a un QR de 4 colores, con la pista:
> !!Un unicornio se ha tragado mi otro código QR!! ¿O quizás es otro tipo de código?

![Código 2D multicolor](https://i.imgur.com/AQfEBrG.png)

Si uno se pasea por la [lista de códigos 2D de la wikipedia,](https://en.wikipedia.org/wiki/Barcode#Matrix_(2D%29_barcodes)
se encontrará con los llamados *JAB Codes*, y una búsqueda rápida por
internet revela la página https://jabcode.org. Aquí, puedes escanear
la imagen directamente para obtener el la flag.

> Odio cuando el creador de un reto de CTF añade texto extra sólo porque necesita complejidad en alguna parte. ETSIIT_CTF{V1rtu+L_C00ff33_sP1ll}







FROM php:8.0-apache

# CONFIGURACION CON ROOT
USER root

COPY flag.txt /flag.txt
RUN chmod 664 /flag.txt

WORKDIR /var/www/html

### Añadir archivos del servidor
COPY apacheFiles /var/www/html

### Configure ownership
RUN chown www-data:www-data -R /var/www/html

# CONFIGURACION DEL SERVIDOR CON EL USUARIO www-data
USER www-data

EXPOSE 80/tcp

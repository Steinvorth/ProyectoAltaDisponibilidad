#!/bin/bash

# Listar los contenidos del directorio de scripts de base de datos para verificación
echo "Listando los contenidos del directorio /usr/src/app/database..."
ls -l /usr/src/app/database

# Esperar a que los contenedores de la base de datos estén listos
echo "Esperando a los contenedores de la base de datos..."
sleep 20

# Ejecutar el script de la base de datos principal en janus-mysql-main
echo "Inicializando la base de datos PRINCIPAL..."
mysql -h janus-mysql-main -P 3306 -u root -p123456789 < /usr/src/app/database/db_script_MAIN.txt

# Ejecutar el script de la base de datos de respaldo en janus-mysql-respaldo
echo "Inicializando la base de datos de RESPALDO..."
mysql -h janus-mysql-respaldo -P 3306 -u root -p123456789 < /usr/src/app/database/db_script_RESPALDO.txt

echo "¡Bases de datos inicializadas!"

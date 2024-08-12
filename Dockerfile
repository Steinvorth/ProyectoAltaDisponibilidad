FROM node:18

# Install the MySQL client
RUN apt-get update && apt-get install -y default-mysql-client

# Usar el directorio de trabajo como el directorio actual en el contenedor
WORKDIR /usr/src/app

# Copiar los archivos del proyecto al contenedor
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto de los archivos al contenedor
COPY . .

# Hacer el script de inicialización de las bases de datos ejecutable
RUN chmod +x /usr/src/app/init-db.sh

# Puerto de la aplicacion
EXPOSE 3008

# Iniciar la aplicacion
CMD ["sh", "-c", "/usr/src/app/init-db.sh && node server.js"]

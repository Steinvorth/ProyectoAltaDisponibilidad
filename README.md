# Proyecto Alta Disponibilidad

Este es un proyecto desarrollado como parte del curso **Alta Disponibilidad**. El propósito de este proyecto es ilustrar conceptos relacionados con la alta disponibilidad utilizando tecnologías como Docker, MySQL y Node.js.

**Nota Importante:** Todo el código proporcionado en este repositorio es solo para fines de ejemplo. El uso de alta disponibilidad y las configuraciones presentadas han sido implementadas como demostraciones y no están necesariamente optimizadas para un entorno de producción.

## Contenido del Proyecto

El proyecto está compuesto por los siguientes elementos:

- **Servidor Node.js:** La aplicación principal que se ejecuta en un contenedor Docker.
- **Bases de Datos MySQL:** Dos contenedores de MySQL que simulan un entorno de alta disponibilidad.

## Instrucciones de Uso

### Requisitos

- Docker y Docker Compose instalados en el sistema.

### Iniciar el Proyecto

1. Clonar este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/ProyectoAltaDisponibilidad.git
   cd ProyectoAltaDisponibilidad
   ```

2. Construir y levantar los contenedores:
   ```
   docker compose up --build
   ```

3. La aplicación estará disponible en `http://localhost:3008`.

### Funcionalidades

- **Administración de Usuarios y Carros:** La aplicación permite la gestión de usuarios y vehículos a través de una interfaz sencilla.
- **Simulación de Alta Disponibilidad:** Se simula un entorno de alta disponibilidad mediante la duplicación de bases de datos MySQL en contenedores separados.

## Consideraciones Finales

Este proyecto es una simulación y se ha desarrollado únicamente con fines educativos. No se recomienda su uso en un entorno de producción sin las modificaciones y optimizaciones necesarias.


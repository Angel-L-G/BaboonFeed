# BaboonFeed

![BaboonFeed-Logo](BaboonFeedLogo.jpg)

**BaboonFeed** es una red social cuyo objetivo es permitir la libre expresión del humor sin depender de reglas estrictas. Sin embargo, "sin muchas reglas" no significa total libertad: siempre debe tratarse de humor y expresarse desde el respeto. Cualquier comentario que no cumpla con estas normas será eliminado, y el usuario recibirá un aviso.

## Características principales

### Feed interactivo

- BaboonFeed ofrece un flujo de contenido donde se mostrarán las publicaciones de los usuarios.
- Puedes darle "me gusta" o "no me gusta" a las publicaciones y comentar en ellas para expresar tu opinión o añadir algo a la conversación.

### Interacción social

- Es posible seguir a otros usuarios.
- Existe la posibilidad de comentar tanto en publicaciones.

### Mensajería

- BaboonFeed incluye un sistema de chat que permite:
  - Enviar mensajes privados a otros usuarios.
  - Crear chats grupales para hablar con varios usuarios.
  - Ambos permiten compartir imágenes, videos y audios.

## Seguridad y verificación

Nuestra plataforma cuenta con un sistema de seguridad basado en un registro y verificación por correo electrónico. El proceso es el siguiente:

1. Durante el registro, se genera una clave única para cada usuario.
2. Se envía un correo electrónico al email registrado por el usuario.
3. Este correo contiene un enlace y/o un botón para verificar la cuenta.
4. Una vez que el usuario verifica su correo, podrá acceder a su cuenta mediante un inicio de sesión simple.

---

## Paleta de Colores

| Nombre      | Hex       |
| ----------- | --------- |
| `primary`   | `#f39c12` |
| `secondary` | `#34495e` |
| `success`   | `#2ecc71` |
| `info`      | `#3498db` |
| `warning`   | `#f1c40f` |
| `danger`    | `#e74c3c` |
| `light`     | `#ecf0f1` |
| `dark`      | `#2c3e50` |
| `purple`    | `#8e44ad` |
| `pink`      | `#ff69b4` |
| `cyan`      | `#17a2b8` |

---

## Backend

| Paquete                         | Descripción breve                                                                                                                      |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `django`                        | Framework web principal, robusto y completo para construir aplicaciones web en Python.                                                 |
| `djangorestframework`           | Extensión de Django para construir APIs RESTful de manera rápida y flexible.                                                           |
| `djangorestframework-simplejwt` | Proporciona autenticación JWT (JSON Web Tokens) para APIs creadas con DRF.                                                             |
| `channels`                      | Permite soporte para WebSockets y otras conexiones asíncronas en Django.                                                               |
| `channels-redis`                | Backend basado en Redis para manejar la capa de canales (asíncrona/pub-sub).                                                           |
| `daphne`                        | Servidor ASGI (Asynchronous Server Gateway Interface) compatible con Django Channels.                                                  |
| `pillow`                        | Librería de procesamiento de imágenes en Python, necesaria para trabajar con campos de imagen en Django.                               |
| `ipython`                       | Intérprete interactivo de Python con mejoras útiles para debugging y exploración.                                                      |
| `prettyconf`                    | Gestor de configuración basado en variables de entorno, útil para separar configuración de código.                                     |
| `django-cors-headers`           | Middleware para manejar CORS (Cross-Origin Resource Sharing) en Django, esencial al conectar frontend y backend en dominios distintos. |
| `psycopg2`                      | Driver de PostgreSQL para Python, necesario si usas PostgreSQL como base de datos.                                                     |

---

## Frontend

| Paquete                               | Descripción breve                                                                                      |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `vue`                                 | Framework progresivo de JavaScript para construir interfaces de usuario.                               |
| `axios`                               | Cliente HTTP para realizar peticiones a APIs desde el frontend.                                        |
| `bootstrap`                           | Framework de diseño CSS con componentes listos para usar y estilos responsivos.                        |
| `date-fns`                            | Librería para manipulación de fechas con funciones puras y modulares.                                  |
| `dayjs`                               | Alternativa ligera a Moment.js para manejo de fechas y tiempos.                                        |
| `fontawesome`                         | Versión antigua del paquete Font Awesome.                                                              |
| `json-server`                         | Servidor mock que convierte un archivo JSON en una API REST completa; útil para desarrollo.            |
| `pinia`                               | Librería oficial de gestión de estado para Vue 3 (reemplazo moderno de Vuex).                          |
| `plyr`                                | Reproductor de video/audio moderno, accesible y personalizable.                                        |
| `reconnecting-websocket`              | WebSocket con reconexión automática, útil para mantener conexiones en tiempo real.                     |
| `sass`                                | Preprocesador CSS con variables, funciones y anidamiento, esencial para estilos avanzados.             |
| `vue-plyr`                            | Envoltorio de Vue para integrar fácilmente `plyr` como componente.                                     |
| `vue-router`                          | Sistema de ruteo oficial para Vue 3, permite crear SPA con navegación entre vistas.                    |

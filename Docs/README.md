# BaboonFeed

## Requisitos técnicos del Proyecto

- Construido con Vue 3
  - Creación del proyecto con:
    ```sh
    npm create vue@latest
    ```
  - Opciones seleccionadas durante la configuración:
    - TypeScript
    - Vue Router
    - Pinia
    - ESLint
    - Vitest
- Librerías adicionales:
  - i18n (para traducciones)
- Framework de estilos CSS utilizado: Bootstrap con Sass para modificarlo.

## Hacer uso de

- **Composition API** para la gestión de estado y funcionalidades de los componentes.
- **Formato SFC (Single File Components)** en los componentes.
- **Uso de TypeScript** para tipado estricto y mejor mantenibilidad del código.
- **Vue Router** para la gestión de navegación por URL.
- **Barra de navegación** para la estructura de la aplicación.
- **Props y emit** para la comunicación entre componentes padre-hijo consecutivos en el DOM.
- **Directivas** personalizadas para mejorar la reutilización del código.
- **Slot** para definir el componente base del producto de la tienda.
- **Provide/Inject** para la comunicación entre componentes padre-hijo distanciados en la misma rama del DOM.
- **Pinia** para compartir datos globales y accesibles desde otros componentes.
- **Composable** para acceder a la base de datos.
- **Fetch API** para la obtención de datos.
- **Traducción de la aplicación** a dos idiomas (Español y [Otro idioma]).
- **Uso de interfaces** para definir estructuras de datos tipadas.

## Instalación

1. Clonar el repositorio:
   ```sh
   git clone https://github.com/Angel-L-G/BaboonFeed.git
   cd BaboonFeed
   ```
2. Instalar dependencias:
   ```sh
   npm install
   ```
3. Ejecutar el servidor en modo desarrollo:
   ```sh
   npm run dev
   ```
   La aplicación estará disponible en `http://localhost:5173`.

## Tests

- **Test unitarios**: Se realizan pruebas con Vitest para garantizar el correcto funcionamiento de los componentes.
- **Test de componentes**: Validación de props, eventos y comportamiento esperado.

Para ejecutar las pruebas:
```sh
npm run test
```

## Estructura del Proyecto

```
BaboonFeed/
│-- src/
│   ├── components/   # Componentes reutilizables
│   ├── views/        # Vistas principales
│   ├── store/        # Pinia store
│   ├── router/       # Configuración del router
│   ├── i18n/         # Configuración de idiomas
│   ├── assets/       # Recursos estáticos
│   ├── tests/        # Pruebas unitarias
│   ├── plugins/      # Configuración de distintas librerias
│   └── main.ts       # Punto de entrada principal
│-- package.json      # Configuración del proyecto
│-- vite.config.ts    # Configuración de Vite
```

## Buenas prácticas y calidad del código

- Código comentado y bien documentado.
- Estructura limpia y ordenada.
- Uso de buenas prácticas de programación.
- Modularidad y reutilización de componentes.



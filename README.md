# Conduce Seguro

Este proyecto es una aplicación web para una autoescuela llamada "Conduce Seguro". Permite la gestión de alumnos, instructores, vehículos y prácticas, además de ofrecer información sobre la autoescuela y un formulario de inscripción.

## Cómo ejecutar el proyecto

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

1.  **Clonar el repositorio:**

    ```bash
    https://github.com/Zprit3/Proyecto_Certificacion_Bootcamp_Python.git
    ```

2.  **Crear un entorno virtual:**

    ```bash
    python3 -m venv .venv       # Crea el entorno virtual
    source .venv/bin/activate  # Activa el entorno virtual (Linux/macOS)
    .venv\Scripts\activate     # Activa el entorno virtual (Windows)
    ```

3.  **Instalar las dependencias:**
    requirements.txt esta en la raiz del proyecto, solo usar el comando pip y listo
    ```bash
    pip install -r requirements.txt
    ```

4.  **Migrar la base de datos:**

    ```bash
    python manage.py migrate
    ```

5.  **Crear un superusuario (opcional, para acceder al panel de administración):**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Ejecutar el servidor de desarrollo:**

    ```bash
    python manage.py runserver
    ```

7.  **Abrir el navegador:**

    Abre tu navegador web y navega a `http://127.0.0.1:8000/` o `http://localhost:8000/`.

## Dependencias

Las dependencias del proyecto se encuentran en el archivo `requirements.txt`.

## Tecnologías utilizadas

*   Python
*   Django
*   Bootstrap 5


## Estructura del proyecto


*   `gestion/`: Aplicación para la gestión de la autoescuela.
*   `landing/`: Aplicación para las páginas públicas (inicio, nosotros, etc.).
*   `templates/`: Plantillas HTML.
*   `static/`: Archivos estáticos (CSS, JavaScript).

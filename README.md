# Sistema de Asistencia con Validación Facial

Aplicativo web desarrollado en Django y OpenCV para registrar la asistencia de usuarios. El sistema utiliza un formulario para capturar datos y una validación de "prueba de vida" (liveness check) para verificar al usuario antes de guardar el registro en una base de datos.

## 🚀 Funcionalidades

* **Formulario de Registro:** Captura los datos del usuario (Nombre, Apellido, Curso, Materia).
* **Base de Datos:** Almacena todos los registros de asistencia en una base de datos SQLite.
* **Validación de Prueba de Vida:** Antes de guardar, el sistema activa la cámara y pide al usuario que **mire de frente** y luego **incline la cabeza**. Esto previene el uso de fotos.
* **Captura Automática:** Al pasar la validación, el sistema guarda automáticamente una foto (tomada de frente) junto con los datos del formulario.
* **Galería de Asistencias:** La página principal muestra una tabla con todos los registros guardados, incluyendo la foto, datos y fecha.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python
* **Framework:** Django
* **Visión por Computadora:** OpenCV (cv2)
* **Manejo de Imágenes:** Pillow
* **Frontend:** HTML, CSS, JavaScript (Fetch API)

## 📋 Guía de Instalación y Ejecución

Sigue estos pasos para ejecutar el proyecto localmente:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Arthuro2003/Detector_de_rostro.git](https://github.com/Arthuro2003/Detector_de_rostro.git)
    cd Detector_de_rostro
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    # Crear el entorno
    python -m venv venv
    
    # Activar en Linux/Mac
    source venv/bin/activate
    
    # Activar en Windows
    # venv\Scripts\activate
    ```

3.  **Instalar las dependencias:**
    *(Esto instalará Django, OpenCV, Pillow, etc.)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Descargar el clasificador de OpenCV:**
    * Este proyecto requiere el clasificador de **rostros frontales**.
    * Descarga el archivo: `haarcascade_frontalface_default.xml` desde [**este enlace**](https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml).
    * Guárdalo en la **carpeta raíz del proyecto** (al mismo nivel que `manage.py`).

5.  **Crear la Base de Datos (Migraciones):**
    ```bash
    python manage.py makemigrations app
    python manage.py migrate
    ```

6.  **Ejecutar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

7.  **Abrir el aplicativo:**
    Abre tu navegador y ve a `http://127.0.0.1:8000/`.

## ⚙️ Cómo Usar

1.  Abre la aplicación en `http://127.0.0.1:8000/`.
2.  Llena el formulario con tus datos y presiona "Continuar a Validación Facial".
3.  Serás redirigido a la página de validación.
4.  Sigue las instrucciones en pantalla: "Mire de frente a la cámara...".
5.  Cuando el texto cambie a "¡Bien! Ahora incline la cabeza.", inclina tu cabeza hacia un lado.
6.  El sistema te validará, guardará tu asistencia y te redirigirá a la página principal.
7.  Tu registro (con foto) aparecerá en la parte superior de la tabla de asistencias.

## 📸 Vistazo del Proyecto
<img width="786" height="355" alt="imagen" src="https://github.com/user-attachments/assets/9677d6be-f522-46b0-a2de-1a8fe5d11b04" />


<img width="848" height="412" alt="imagen" src="https://github.com/user-attachments/assets/cb23e5f8-c5d1-4691-9c2d-2dac1607e32d" />

# Detector de Rostros Interactivo (Django + OpenCV)

Aplicativo web desarrollado como parte de la Práctica Experimental de la asignatura **Construcción de Software**. El sistema utiliza Django para el backend y OpenCV para el procesamiento de video en tiempo real.

## 🚀 Funcionalidades Principales

* **Streaming en Tiempo Real:** Transmite video en vivo desde la cámara web del usuario.
* **Detección de Rostros:** Utiliza Haar Cascades de OpenCV para detectar rostros en el video.
* **Contador de Rostros:** Muestra un conteo en vivo de los rostros detectados.
* **Captura Manual:** Un botón permite al usuario tomar una captura de pantalla del video, la cual incluye las anotaciones (rectángulos y contadores).
* **Captura Automática:** El sistema guarda una captura automáticamente (sin anotaciones) cuando detecta un rostro por primera vez.
* **Temporizador (Cooldown):** Después de una captura automática, se activa un temporizador de 1 hora para evitar capturas duplicadas.
* **Galería de Capturas:** Muestra todas las capturas manuales y automáticas en una galería interactiva.
* **Limpiar Galería:** Un botón permite eliminar todos los archivos de capturas del servidor.

## 🛠️ Tecnologías Utilizadas

* [cite_start]**Backend:** Python [cite: 60]
* [cite_start]**Framework:** Django [cite: 61]
* [cite_start]**Visión por Computadora:** OpenCV (cv2) [cite: 62]
* **Frontend:** HTML, CSS y JavaScript (con Fetch API).

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
    ```bash
    pip install -r requirements.txt
    ```

4.  **Descargar el clasificador de OpenCV:**
    * Descarga el archivo `haarcascade_frontalface_default.xml` desde [este enlace](https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml).
    * Guárdalo en la **carpeta raíz del proyecto** (al mismo nivel que `manage.py`).

5.  **Aplicar las migraciones de Django:**
    ```bash
    python manage.py migrate
    ```

6.  **Ejecutar el servidor de desarrollo:**
    ```bash
    python manage.py runserver
    ```

7.  **Abrir el aplicativo:**
    Abre tu navegador y ve a `http://127.0.0.1:8000/`.

## 📸 Vistazo del Proyecto

<img width="1919" height="968" alt="imagen" src="https://github.com/user-attachments/assets/4f87e181-2d74-40e6-82be-6461f026b2c9" />


# app/views.py

from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from .camera import cam  # <-- Importamos la INSTANCIA global 'cam'
import os
import datetime
from django.conf import settings


# --- VISTA INDEX MODIFICADA ---
# Ahora escanea la carpeta de capturas y las envía a la plantilla
def index(request):
    captures_dir = os.path.join(settings.MEDIA_ROOT, 'captures')
    image_files = []

    # Nos aseguramos de que el directorio exista
    if os.path.exists(captures_dir):
        # Listamos los archivos y los ordenamos por fecha de modificación (más nuevos primero)
        files = sorted(
            [f for f in os.listdir(captures_dir) if f.endswith('.jpg')],
            key=lambda f: os.path.getmtime(os.path.join(captures_dir, f)),
            reverse=True
        )

        for filename in files:
            filepath = os.path.join(captures_dir, filename)
            mtime = os.path.getmtime(filepath)
            image_files.append({
                'url': os.path.join(settings.MEDIA_URL, 'captures', filename),
                'timestamp': datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            })

    return render(request, 'index.html', {'images': image_files})


# --- VISTA GEN MODIFICADA ---
# Ya no necesita el argumento 'camera', usa la global 'cam'
def gen():
    while True:
        frame = cam.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# --- VISTA VIDEO_FEED MODIFICADA ---
def video_feed(request):
    return StreamingHttpResponse(gen(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


# --- VISTA NUEVA: Para el botón "Tomar Captura" ---
def capture_snapshot(request):
    file_url, timestamp = cam.save_manual_capture()
    if file_url:
        return JsonResponse({'status': 'ok', 'url': file_url, 'timestamp': timestamp})
    else:
        return JsonResponse({'status': 'error', 'message': 'No se pudo capturar la imagen'})


# --- VISTA NUEVA: Para el botón "Limpiar Capturas" ---
def clear_captures(request):
    try:
        captures_dir = os.path.join(settings.MEDIA_ROOT, 'captures')
        for filename in os.listdir(captures_dir):
            if filename.endswith('.jpg'):
                os.remove(os.path.join(captures_dir, filename))
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
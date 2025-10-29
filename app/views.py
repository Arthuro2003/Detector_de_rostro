# app/views.py

from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, JsonResponse
from .models import Asistencia
from .forms import AsistenciaForm
# --- Importamos la nueva instancia de la cámara ---
from .camera import liveness_cam
import time


# Vista index (sin cambios)
def index(request):
    if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            return redirect('validate_view')
    else:
        form = AsistenciaForm()
    asistencias_registradas = Asistencia.objects.all().order_by('-fecha_registro')
    context = {
        'form': form,
        'asistencias': asistencias_registradas
    }
    return render(request, 'index.html', context)


# Vista validate_view (sin cambios)
def validate_view(request):
    form_data = request.session.get('form_data')
    if not form_data:
        return redirect('index')

    # Reseteamos el estado de la cámara cada vez que se carga la página
    liveness_cam.__init__()  # Reinicia la cámara y los contadores

    return render(request, 'validate.html')


# --- FUNCIÓN GENERADORA MODIFICADA ---
def gen(camera):
    while True:
        frame_bytes, status, success = camera.get_frame()

        if frame_bytes:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

        # Enviamos el estado como una cabecera HTTP
        # (El JS no puede leer esto, usaremos el endpoint de status)
        # Lo dejamos por si acaso, pero crearemos un endpoint mejor

        if success:
            print("Validación exitosa, deteniendo stream.")
            break  # Detiene el generador si la validación fue exitosa

        time.sleep(0.05)  # Pequeña pausa para no sobrecargar el CPU


# --- VISTA VIDEO_FEED MODIFICADA ---
def video_feed(request):
    # Usamos la instancia global 'liveness_cam'
    return StreamingHttpResponse(gen(liveness_cam),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


# --- VISTA NUEVA: Para que el JS pregunte el estado ---
def validation_status(request):
    """
    Provee al frontend el estado actual de la validación.
    """
    return JsonResponse({
        'status': liveness_cam.status,
        'success': liveness_cam.validation_success
    })


# --- VISTA NUEVA: Para guardar la asistencia ---
def process_validation(request):
    """
    Se llama desde JS cuando 'validation_status' devuelve success=True.
    Guarda la asistencia en la BD.
    """
    if request.method == 'POST':
        form_data = request.session.get('form_data')
        if not form_data:
            return JsonResponse({'status': 'error', 'message': 'Sesión expirada.'})

        # Usamos la instancia de la cámara para guardar la foto
        success, message = liveness_cam.save_assistance(form_data)

        if success:
            # Limpiamos la sesión después de guardar
            request.session.pop('form_data', None)
            return JsonResponse({'status': 'ok', 'message': message})
        else:
            return JsonResponse({'status': 'error', 'message': message})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})
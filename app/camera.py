# app/camera.py

import cv2
import os
import datetime
from django.conf import settings


class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.last_capture_time = None
        self.cooldown_seconds = 3600  # 1 hora

        self.captures_dir = os.path.join(settings.MEDIA_ROOT, 'captures')
        os.makedirs(self.captures_dir, exist_ok=True)

    def __del__(self):
        self.video.release()

    # --- NUEVO MÉTODO INTERNO ---
    # Esta función centraliza TODAS las anotaciones (textos y rectángulos)
    def _build_annotated_frame(self, image, now):
        # 1. Detección
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        face_count = len(faces)

        # 2. Anotación de texto (Contador)
        text = f"Rostros detectados: {face_count}"
        cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # Verde

        # 3. Anotación de texto (Cooldown)
        if self.last_capture_time:
            time_left = self.cooldown_seconds - (now - self.last_capture_time).total_seconds()
            if time_left > 0:
                minutes, seconds = divmod(int(time_left), 60)
                cooldown_text = f"Cooldown Auto: {minutes:02d}:{seconds:02d}"
                cv2.putText(image, cooldown_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # Rojo
            else:
                cv2.putText(image, "LISTO PARA CAPTURA AUTO", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            2)  # Verde

        # 4. Anotación de rectángulos
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Azul

        # Devolvemos la imagen anotada y el conteo de rostros
        return image, face_count

    # --- FUNCIÓN get_frame MODIFICADA ---
    def get_frame(self):
        success, image = self.video.read()
        if not success:
            # En caso de error, simplemente devolvemos la última imagen exitosa (si existe)
            # O un frame vacío, pero por ahora asumimos que funciona
            return

        # Guardamos una copia limpia para la captura automática
        clean_image = image.copy()
        now = datetime.datetime.now()

        # Usamos la nueva función para añadir TODAS las anotaciones a la imagen
        annotated_image, face_count = self._build_annotated_frame(image, now)

        # Lógica de captura automática (sin cambios)
        # Sigue guardando la imagen LIMPIA (sin anotaciones)
        if face_count > 0:
            take_capture = False
            if self.last_capture_time is None:
                take_capture = True
            else:
                time_since_last_capture = (now - self.last_capture_time).total_seconds()
                if time_since_last_capture > self.cooldown_seconds:
                    take_capture = True

            if take_capture:
                filename = f"auto_captura_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
                filepath = os.path.join(self.captures_dir, filename)
                cv2.imwrite(filepath, clean_image)  # Guarda la imagen limpia
                self.last_capture_time = now
                print(f"Captura automática guardada en: {filepath}")

        # Codificamos la imagen ANOTADA para el stream
        ret, jpeg = cv2.imencode('.jpg', annotated_image)
        return jpeg.tobytes()

    # --- FUNCIÓN save_manual_capture MODIFICADA ---
    def save_manual_capture(self):
        success, image = self.video.read()
        if success:
            now = datetime.datetime.now()

            # --- AQUÍ ESTÁ EL CAMBIO ---
            # Aplicamos las MISMAS anotaciones que el stream
            annotated_image, _ = self._build_annotated_frame(image, now)

            filename = f"manual_captura_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(self.captures_dir, filename)

            # Guardamos la imagen ANOTADA
            cv2.imwrite(filepath, annotated_image)

            file_url = os.path.join(settings.MEDIA_URL, 'captures', filename)
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
            return file_url, timestamp
        return None, None


# --- Instancia global (sin cambios) ---
cam = VideoCamera()
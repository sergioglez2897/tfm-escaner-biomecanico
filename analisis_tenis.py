import cv2
import mediapipe as mp
import numpy as np
import os
import csv

# ==========================================
# CONFIGURACIÓN DEL JUGADOR
# ==========================================
NOMBRE_JUGADOR = "Nadal" 
VIDEO_ENTRADA = "Derecha_Nadal.mp4" # <--- Cambia esto si tu vídeo se llama diferente
REFRESCO_VISUAL = 5  
# ==========================================

dir_actual = os.path.dirname(os.path.abspath(__file__))
path_entrada = os.path.join(dir_actual, VIDEO_ENTRADA)
video_salida = os.path.join(dir_actual, f"Analisis_{NOMBRE_JUGADOR}_Legible.mp4")
csv_salida = os.path.join(dir_actual, f"datos_{NOMBRE_JUGADOR}.csv")

def calcular_angulo(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radianes = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angulo = np.abs(radianes * 180.0 / np.pi)
    return 360 - angulo if angulo > 180.0 else angulo

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# --- Configuración de dibujo SÚPER LEGIBLE ---
espec_puntos = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=-1, circle_radius=6)
espec_lineas = mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=4)

cap = cv2.VideoCapture(path_entrada)

if not cap.isOpened():
    print(f"❌ ERROR: No encuentro el vídeo '{VIDEO_ENTRADA}' en la carpeta.")
    exit()

w, h = int(cap.get(3)), int(cap.get(4))
fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0: fps = 30
writer = cv2.VideoWriter(video_salida, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

datos_log = []
frame_count = 0
prev_wrist = None
disp_codo, disp_hombro, disp_rodilla, disp_vel = 0, 0, 0, 0

print(f"🚀 Analizando a {NOMBRE_JUGADOR} con Dashboard gigante...")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame_count += 1
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = pose.process(img_rgb)

        if res.pose_landmarks:
            lm = res.pose_landmarks.landmark
            
            # Puntos clave (Brazo/Pierna derecha)
            hombro = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
            codo = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW].x, lm[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
            muneca = [lm[mp_pose.PoseLandmark.RIGHT_WRIST].x, lm[mp_pose.PoseLandmark.RIGHT_WRIST].y]
            cadera = [lm[mp_pose.PoseLandmark.RIGHT_HIP].x, lm[mp_pose.PoseLandmark.RIGHT_HIP].y]
            rodilla = [lm[mp_pose.PoseLandmark.RIGHT_KNEE].x, lm[mp_pose.PoseLandmark.RIGHT_KNEE].y]
            tobillo = [lm[mp_pose.PoseLandmark.RIGHT_ANKLE].x, lm[mp_pose.PoseLandmark.RIGHT_ANKLE].y]

            # Ángulos
            ang_codo = calcular_angulo(hombro, codo, muneca)
            ang_hombro = calcular_angulo(cadera, hombro, codo)
            ang_rodilla = calcular_angulo(cadera, rodilla, tobillo)
            
            # Velocidad de muñeca
            vel = 0
            curr_wrist = np.array([muneca[0]*w, muneca[1]*h])
            if prev_wrist is not None:
                vel = np.linalg.norm(curr_wrist - prev_wrist) * (fps / 10)
            prev_wrist = curr_wrist

            # Guardar en log para CSV
            datos_log.append([frame_count, round(ang_codo, 1), round(ang_hombro, 1), round(ang_rodilla, 1), round(vel, 1)])
            
            # Actualizar números en pantalla solo cada 5 frames
            if frame_count % REFRESCO_VISUAL == 0:
                disp_codo, disp_hombro, disp_rodilla, disp_vel = int(ang_codo), int(ang_hombro), int(ang_rodilla), int(vel)

            # --- DASHBOARD GIGANTE ---
            overlay = frame.copy()
            cv2.rectangle(overlay, (20, 20), (520, 280), (0, 0, 0), -1) 
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame) 

            # Textos grandes (fontScale=1.2, thickness=3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            color_txt = (255, 255, 255)
            cv2.putText(frame, f"Codo: {disp_codo} deg", (40, 70), font, 1.2, color_txt, 3)
            cv2.putText(frame, f"Hombro: {disp_hombro} deg", (40, 130), font, 1.2, color_txt, 3)
            cv2.putText(frame, f"Rodilla: {disp_rodilla} deg", (40, 190), font, 1.2, color_txt, 3)
            cv2.putText(frame, f"Vel: {disp_vel} px/s", (40, 250), font, 1.2, (0, 255, 255), 3)

            # Dibujar esqueleto marcado
            mp_drawing.draw_landmarks(
                frame, 
                res.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                espec_puntos, 
                espec_lineas
            )

        writer.write(frame)

finally:
    cap.release()
    writer.release()
    # Guardar CSV
    if len(datos_log) > 0:
        with open(csv_salida, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(['Frame', 'Codo', 'Hombro', 'Rodilla', 'Velocidad_Muñeca'])
            escritor.writerows(datos_log)
        print(f"✅ ¡VÍDEO DE DJOKOVIC LISTO!")
        print(f"📁 Tienes el vídeo 'Analisis_{NOMBRE_JUGADOR}_Legible.mp4' y los datos en 'datos_{NOMBRE_JUGADOR}.csv'")
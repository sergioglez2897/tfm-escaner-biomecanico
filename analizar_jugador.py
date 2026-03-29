import cv2
import mediapipe as mp
import numpy as np
import os
import csv

# ==========================================
# CONFIGURACIÓN DEL JUGADOR
# ==========================================
# Cambia esto para cada jugador (Alcaraz, Sinner, Djokovic, Nadal)
NOMBRE_JUGADOR = "Sinner" 
VIDEO_ENTRADA = "Derecha_Sinner.mp4" # <--- Asegúrate de que el nombre sea exacto
REFRESCO_VISUAL = 5  
# ==========================================

dir_actual = os.path.dirname(os.path.abspath(__file__))
path_entrada = os.path.join(dir_actual, VIDEO_ENTRADA)
video_salida = os.path.join(dir_actual, f"Analisis_{NOMBRE_JUGADOR}_Premium.mp4")
csv_salida = os.path.join(dir_actual, f"datos_{NOMBRE_JUGADOR}_premium.csv")

# Función para calcular el ángulo entre tres puntos
def calcular_angulo(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radianes = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angulo = np.abs(radianes * 180.0 / np.pi)
    return 360 - angulo if angulo > 180.0 else angulo

# Función para calcular el ángulo de una línea respecto a la horizontal
def calcular_angulo_horizontal(p1, p2):
    p1, p2 = np.array(p1), np.array(p2)
    delta_y = p2[1] - p1[1]
    delta_x = p2[0] - p1[0]
    radianes = np.arctan2(delta_y, delta_x)
    angulo = np.abs(radianes * 180.0 / np.pi)
    return angulo

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Configuración de dibujo SÚPER LEGIBLE (puntos y líneas gordas)
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
prev_nose_y = None

# Variables para el Dashboard (refresco cada 5 frames)
disp_codo, disp_hombro_rot, disp_cadera_rot, disp_sep, disp_rodilla, disp_vel_mun, disp_est_cab = 0, 0, 0, 0, 0, 0, 0

print(f"🚀 Iniciando Análisis PREMIUM de 8 puntos para {NOMBRE_JUGADOR}...")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        frame_count += 1
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = pose.process(img_rgb)

        if res.pose_landmarks:
            lm = res.pose_landmarks.landmark
            
            # --- CAPTURA DE LOS 8 PUNTOS CLAVE (Lado Derecho/Dominante asumido) ---
            # 1. Nariz (Estabilidad Cabeza)
            nariz = [lm[mp_pose.PoseLandmark.NOSE].x, lm[mp_pose.PoseLandmark.NOSE].y]
            # 2. Hombro Dominante
            hombro_d = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
            # 3. Codo Dominante
            codo_d = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW].x, lm[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
            # 4. Muñeca Dominante
            muneca_d = [lm[mp_pose.PoseLandmark.RIGHT_WRIST].x, lm[mp_pose.PoseLandmark.RIGHT_WRIST].y]
            # 5. Cadera Trasera (asumimos derecha para inicio giro)
            cadera_t = [lm[mp_pose.PoseLandmark.RIGHT_HIP].x, lm[mp_pose.PoseLandmark.RIGHT_HIP].y]
            # 6. Cadera Delantera (izquierda para ver rotación completa)
            cadera_d = [lm[mp_pose.PoseLandmark.LEFT_HIP].x, lm[mp_pose.PoseLandmark.LEFT_HIP].y]
            # 7. Rodilla Delantera (izquierda)
            rodilla_d = [lm[mp_pose.PoseLandmark.LEFT_KNEE].x, lm[mp_pose.PoseLandmark.LEFT_KNEE].y]
            # 8. Tobillo Delantero (izquierda)
            tobillo_d = [lm[mp_pose.PoseLandmark.LEFT_ANKLE].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE].y]
            # Punto extra para ángulo rodilla (cadera delantera)
            # cadera_d ya definida

            # --- CÁLCULOS BIOMECÁNICOS AVANZADOS ---
            
            # A. Ángulos Articulares Clásicos
            ang_codo = calcular_angulo(hombro_d, codo_d, muneca_d)
            ang_rodilla = calcular_angulo(cadera_d, rodilla_d, tobillo_d)
            
            # B. Rotaciones (respecto a la horizontal)
            # Usamos hombro derecho e izquierdo para la línea de hombros
            hombro_i = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
            rot_hombros = calcular_angulo_horizontal(hombro_d, hombro_i)
            rot_caderas = calcular_angulo_horizontal(cadera_t, cadera_d)
            
            # C. Separación Cadera-Hombros (X-Factor)
            separacion = np.abs(rot_hombros - rot_caderas)
            
            # D. Velocidad de Muñeca (Lag)
            vel_mun = 0
            curr_wrist = np.array([muneca_d[0]*w, muneca_d[1]*h])
            if prev_wrist is not None:
                vel_mun = np.linalg.norm(curr_wrist - prev_wrist) * (fps / 10) # Normalizado
            prev_wrist = curr_wrist
            
            # E. Estabilidad de Cabeza (Movimiento vertical de la nariz)
            est_cab = 0
            curr_nose_y = nariz[1] * h
            if prev_nose_y is not None:
                est_cab = np.abs(curr_nose_y - prev_nose_y) # Variación vertical en píxeles
            prev_nose_y = curr_nose_y

            # --- GUARDAR DATOS PREMIUM EN LOG ---
            datos_log.append([
                frame_count, 
                round(ang_codo, 1), 
                round(rot_hombros, 1), 
                round(rot_caderas, 1), 
                round(separacion, 1), 
                round(ang_rodilla, 1), 
                round(vel_mun, 1), 
                round(est_cab, 1)
            ])
            
            # --- ACTUALIZAR DASHBOARD (Cada 5 frames) ---
            if frame_count % REFRESCO_VISUAL == 0:
                disp_codo = int(ang_codo)
                disp_hombro_rot = int(rot_hombros)
                disp_cadera_rot = int(rot_caderas)
                disp_sep = int(separacion)
                disp_rodilla = int(ang_rodilla)
                disp_vel_mun = int(vel_mun)
                disp_est_cab = int(est_cab)

            # --- DIBUJAR DASHBOARD GIGANTE PREMIUM ---
            overlay = frame.copy()
            cv2.rectangle(overlay, (20, 20), (550, 420), (0, 0, 0), -1) 
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame) 

            font = cv2.FONT_HERSHEY_SIMPLEX
            color_txt = (255, 255, 255) 
            color_val = (0, 255, 255) 

            # Columna 1: Ángulos y Rotaciones
            cv2.putText(frame, "--- MECANICA ---", (40, 60), font, 1.1, (100, 255, 100), 3) 
            cv2.putText(frame, f"Codo Armado:", (40, 100), font, 1.0, color_txt, 2)
            cv2.putText(frame, f"{disp_codo} deg", (320, 100), font, 1.0, color_val, 3)
            
            cv2.putText(frame, f"Rot. Hombros:", (40, 140), font, 1.0, color_txt, 2)
            cv2.putText(frame, f"{disp_hombro_rot} deg", (320, 140), font, 1.0, color_val, 3)
            
            cv2.putText(frame, f"Rot. Caderas:", (40, 180), font, 1.0, color_txt, 2)
            cv2.putText(frame, f"{disp_cadera_rot} deg", (320, 180), font, 1.0, color_val, 3)
            
            cv2.putText(frame, f"Sep. C-H (X):", (40, 220), font, 1.0, color_txt, 2)
            cv2.putText(frame, f"{disp_sep} deg", (320, 220), font, 1.0, (255, 100, 100), 3) 

            # Columna 2: Potencia y Estabilidad
            cv2.putText(frame, "--- POTENCIA/ESTAB. ---", (40, 280), font, 1.1, (100, 255, 100), 3)
            cv2.putText(frame, f"Rodilla Apoyo:", (40, 320), font, 1.0, color_txt, 2)
            cv2.putText(frame, f"{disp_rodilla} deg", (320, 320), font, 1.0, color_val, 3)
            
            cv2.putText(frame, f"Vel. Muneca:", (40, 360), font, 1.0, color_txt, 2)
            cv2.putText(frame, f"{disp_vel_mun} px/s", (320, 360), font, 1.0, color_val, 3)
            
            cv2.putText(frame, f"Estab. Cabeza:", (40, 400), font, 1.0, color_txt, 2)
            cv2.putText(frame, f"{disp_est_cab} px-var", (320, 400), font, 1.0, color_val, 3)

            # --- DIBUJAR ESQUELETO MARCADO GORDO ---
            # Dibujamos conexiones completas
            mp_drawing.draw_landmarks(
                frame, 
                res.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                espec_puntos, 
                espec_lineas
            )
            
            # Resaltar específicamente tus 8 puntos clave con círculos rojos más grandes
            puntos_interes = [
                mp_pose.PoseLandmark.NOSE,
                mp_pose.PoseLandmark.RIGHT_SHOULDER,
                mp_pose.PoseLandmark.RIGHT_ELBOW,
                mp_pose.PoseLandmark.RIGHT_WRIST,
                mp_pose.PoseLandmark.RIGHT_HIP,
                mp_pose.PoseLandmark.LEFT_HIP,
                mp_pose.PoseLandmark.LEFT_KNEE,
                mp_pose.PoseLandmark.LEFT_ANKLE
            ]
            
            for idx in puntos_interes:
                landmark = res.pose_landmarks.landmark[idx]
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1) # Círculo rojo gordo

        writer.write(frame)

finally:
    cap.release()
    writer.release()
    # Guardar CSV Premium
    if len(datos_log) > 0:
        with open(csv_salida, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            # Nuevas columnas detalladas
            escritor.writerow([
                'Frame', 
                'Angulo_Codo_Armado', 
                'Rotacion_Hombros_Horizontal', 
                'Rotacion_Caderas_Horizontal', 
                'Separacion_CH_XFactor', 
                'Angulo_Rodilla_Apoyo', 
                'Velocidad_Muneca_Lag', 
                'Estabilidad_Cabeza_VarV'
            ])
            escritor.writerows(datos_log)
        print(f"✅ ¡ANÁLISIS PREMIUM FINALIZADO PARA {NOMBRE_JUGADOR}!")
        print(f"📁 Vídeo: 'Analisis_{NOMBRE_JUGADOR}_Premium.mp4'")
        print(f"📁 Datos CSV: 'datos_{NOMBRE_JUGADOR}_premium.csv'")
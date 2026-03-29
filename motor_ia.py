import cv2
import mediapipe as mp
import numpy as np
import csv

def calcular_angulo(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radianes = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angulo = np.abs(radianes * 180.0 / np.pi)
    return 360 - angulo if angulo > 180.0 else angulo

# --- LA NUEVA MAGIA EN 3D (PLANO TRANSVERSAL) ---
def calcular_rotacion_3d_xz(p1, p2):
    # Usamos la X (ancho) y la Z (profundidad estimada por la IA)
    # Esto simula una cámara colocada en el techo mirando hacia abajo
    delta_z = p2[2] - p1[2]
    delta_x = p2[0] - p1[0]
    radianes = np.arctan2(delta_z, delta_x)
    grados = np.abs(radianes * 180.0 / np.pi)
    # Ajustamos para que siempre sea un ángulo agudo respecto a la red
    if grados > 180.0: grados = 360.0 - grados
    if grados > 90.0: grados = 180.0 - grados
    return grados

def procesar_video_amateur(ruta_entrada, ruta_video_salida, ruta_csv_salida, rotacion="Ninguna"):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils
    espec_puntos = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=-1, circle_radius=6)
    espec_lineas = mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=4)

    cap = cv2.VideoCapture(ruta_entrada)
    if not cap.isOpened(): return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0: fps = 30
    
    ret, test_frame = cap.read()
    if not ret: return False
    
    if rotacion == "Rotar 90º a la Derecha ↻": test_frame = cv2.rotate(test_frame, cv2.ROTATE_90_CLOCKWISE)
    elif rotacion == "Rotar 90º a la Izquierda ↺": test_frame = cv2.rotate(test_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif rotacion == "Rotar 180º (Al revés)": test_frame = cv2.rotate(test_frame, cv2.ROTATE_180)
    
    final_h, final_w = test_frame.shape[:2]
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    writer = cv2.VideoWriter(ruta_video_salida, cv2.VideoWriter_fourcc(*'mp4v'), fps, (final_w, final_h))

    datos_log = []
    frame_count = 0
    prev_wrist, prev_nose_y = None, None
    d_codo, d_hom, d_cad, d_sep, d_rod, d_vel, d_est = 0,0,0,0,0,0,0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        if rotacion == "Rotar 90º a la Derecha ↻": frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        elif rotacion == "Rotar 90º a la Izquierda ↺": frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif rotacion == "Rotar 180º (Al revés)": frame = cv2.rotate(frame, cv2.ROTATE_180)

        frame_count += 1
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = pose.process(img_rgb)

        if res.pose_landmarks:
            lm = res.pose_landmarks.landmark
            nariz = [lm[mp_pose.PoseLandmark.NOSE].x, lm[mp_pose.PoseLandmark.NOSE].y]
            hombro_d = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y, lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].z]
            hombro_i = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y, lm[mp_pose.PoseLandmark.LEFT_SHOULDER].z]
            codo_d = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW].x, lm[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
            muneca_d = [lm[mp_pose.PoseLandmark.RIGHT_WRIST].x, lm[mp_pose.PoseLandmark.RIGHT_WRIST].y]
            cadera_d = [lm[mp_pose.PoseLandmark.RIGHT_HIP].x, lm[mp_pose.PoseLandmark.RIGHT_HIP].y, lm[mp_pose.PoseLandmark.RIGHT_HIP].z]
            cadera_i = [lm[mp_pose.PoseLandmark.LEFT_HIP].x, lm[mp_pose.PoseLandmark.LEFT_HIP].y, lm[mp_pose.PoseLandmark.LEFT_HIP].z]
            rodilla_d = [lm[mp_pose.PoseLandmark.LEFT_KNEE].x, lm[mp_pose.PoseLandmark.LEFT_KNEE].y]
            tobillo_d = [lm[mp_pose.PoseLandmark.LEFT_ANKLE].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE].y]

            # Ángulos Articulares 2D
            ang_codo = calcular_angulo(hombro_d[:2], codo_d, muneca_d)
            ang_rodilla = calcular_angulo(cadera_i[:2], rodilla_d, tobillo_d)
            
            # --- ROTACIONES Y X-FACTOR EN 3D ---
            rot_hombros = calcular_rotacion_3d_xz(hombro_d, hombro_i)
            rot_caderas = calcular_rotacion_3d_xz(cadera_d, cadera_i)
            separacion = np.abs(rot_hombros - rot_caderas)
            
            # Ajuste final de cuadrante por si la cadera y el hombro se cruzan en Z
            if separacion > 90.0:
                separacion = 180.0 - separacion
            
            # Velocidad Muñeca
            vel_mun = 0
            curr_wrist = np.array([muneca_d[0]*final_w, muneca_d[1]*final_h])
            if prev_wrist is not None: vel_mun = np.linalg.norm(curr_wrist - prev_wrist) * (fps / 10)
            prev_wrist = curr_wrist
            
            # Estabilidad Cabeza
            est_cab = 0
            curr_nose_y = nariz[1] * final_h
            if prev_nose_y is not None: est_cab = np.abs(curr_nose_y - prev_nose_y)
            prev_nose_y = curr_nose_y

            datos_log.append([frame_count, round(ang_codo, 1), round(rot_hombros, 1), round(rot_caderas, 1), round(separacion, 1), round(ang_rodilla, 1), round(vel_mun, 1), round(est_cab, 1)])
            
            if frame_count % 5 == 0:
                d_codo, d_hom, d_cad, d_sep, d_rod, d_vel, d_est = int(ang_codo), int(rot_hombros), int(rot_caderas), int(separacion), int(ang_rodilla), int(vel_mun), int(est_cab)

            # --- DASHBOARD COMPLETO ---
            overlay = frame.copy()
            cv2.rectangle(overlay, (15, 15), (420, 260), (0, 0, 0), -1) 
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame) 
            
            font, c_txt, c_val = cv2.FONT_HERSHEY_SIMPLEX, (255, 255, 255), (0, 255, 255)
            fs, g = 0.65, 2 
            
            cv2.putText(frame, "--- DIAGNOSTICO 8 PUNTOS ---", (25, 45), font, 0.8, (100, 255, 100), 2) 
            cv2.putText(frame, f"Codo Armado: {d_codo} deg", (25, 80), font, fs, c_txt, g)
            cv2.putText(frame, f"Rot. Hombros(3D): {d_hom} deg", (25, 110), font, fs, c_txt, g)
            cv2.putText(frame, f"Rot. Caderas(3D): {d_cad} deg", (25, 140), font, fs, c_txt, g)
            cv2.putText(frame, f"X-Factor(3D): {d_sep} deg", (25, 170), font, fs, (255, 100, 100), g)
            
            cv2.putText(frame, f"Rodilla (Apoyo): {d_rod} deg", (25, 200), font, fs, c_val, g)
            cv2.putText(frame, f"Vel. Muneca: {d_vel} px/s", (25, 230), font, fs, c_val, g)
            cv2.putText(frame, f"Estab. Cabeza: {d_est} px", (220, 230), font, fs, c_val, g)

            mp_drawing.draw_landmarks(frame, res.pose_landmarks, mp_pose.POSE_CONNECTIONS, espec_puntos, espec_lineas)
            for idx in [0, 11, 13, 15, 23, 24, 25, 27]: 
                landmark = res.pose_landmarks.landmark[idx]
                cv2.circle(frame, (int(landmark.x * final_w), int(landmark.y * final_h)), 10, (0, 0, 255), -1)

        writer.write(frame)

    cap.release()
    writer.release()
    
    if len(datos_log) > 0:
        with open(ruta_csv_salida, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f)
            escritor.writerow(['Frame', 'Angulo_Codo_Armado', 'Rotacion_Hombros_Horizontal', 'Rotacion_Caderas_Horizontal', 'Separacion_CH_XFactor', 'Angulo_Rodilla_Apoyo', 'Velocidad_Muneca_Lag', 'Estabilidad_Cabeza_VarV'])
            escritor.writerows(datos_log)
        return True
    return False
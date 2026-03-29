import matplotlib.pyplot as plt
import csv
import os
import streamlit as st

def generar_graficas_amateur(nombre_base):
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(dir_actual, f"Datos_{nombre_base}.csv")
    
    if not os.path.exists(csv_path):
        st.warning(f"⚠️ Aviso: No se encontró el archivo de datos {csv_path}. Saltando gráficas.")
        return

    frames, codo, sep_ch, rodilla, vel_mun, est_cab = [], [], [], [], [], []
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                frames.append(int(row['Frame']))
                codo.append(float(row['Angulo_Codo_Armado']))
                sep_ch.append(float(row['Separacion_CH_XFactor']))
                rodilla.append(float(row['Angulo_Rodilla_Apoyo']))
                vel_mun.append(float(row['Velocidad_Muneca_Lag']))
                est_cab.append(float(row['Estabilidad_Cabeza_VarV']))

        # --- CÁLCULO DEL PUNTO DE IMPACTO (Frame 0) ---
        # Buscamos el pico de velocidad de la muñeca
        max_vel = max(vel_mun)
        indice_impacto = vel_mun.index(max_vel)
        frame_impacto = frames[indice_impacto]
        
        # Centrar todos los frames para que el impacto coincida con el 0 (Igual que los pros)
        frames_centrados = [f - frame_impacto for f in frames]

        # Configuración estética
        plt.style.use('seaborn-v0_8-muted')
        color_p = "#3498db" # Tu color principal (Azul amateur)

        # ==========================================
        # GRÁFICA 1: CADENA CINÉTICA (X-FACTOR)
        # ==========================================
        fig1 = plt.figure(figsize=(10, 6))
        plt.title(f'TUS DATOS: CADENA CINÉTICA (X-FACTOR)', fontsize=18, fontweight='bold', color=color_p)
        plt.fill_between(frames_centrados, sep_ch, color='#e74c3c', alpha=0.2)
        plt.plot(frames_centrados, sep_ch, color='#c0392b', linewidth=3)
        plt.ylabel('Grados (º)', fontsize=14)
        plt.xlabel('Frames relativos al IMPACTO (0 = Contacto)', fontsize=14)
        
        # LA FAMOSA LÍNEA ROJA
        plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Punto de Impacto')
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        
        ruta_grafica1 = os.path.join(dir_actual, f"Grafica_{nombre_base}_Amateur_Cinematica.png")
        plt.savefig(ruta_grafica1, dpi=300)
        plt.close(fig1)

        # ==========================================
        # GRÁFICA 2: ARTICULACIONES Y POTENCIA
        # ==========================================
        fig2, axs2 = plt.subplots(2, 2, figsize=(14, 10))
        fig2.suptitle(f'TUS DATOS: ARTICULACIONES Y POTENCIA', fontsize=18, fontweight='bold', color=color_p)

        # Codo Armado
        axs2[0, 0].plot(frames_centrados, codo, color=color_p, linewidth=2.5)
        axs2[0, 0].set_title('Ángulo Codo (º)', fontsize=14)

        # Rodilla Apoyo
        axs2[0, 1].plot(frames_centrados, rodilla, color="#e67e22", linewidth=2.5)
        axs2[0, 1].set_title('Ángulo Rodilla Apoyo (º)', fontsize=14)

        # Velocidad Muñeca (Lag)
        axs2[1, 0].fill_between(frames_centrados, vel_mun, color=color_p, alpha=0.2)
        axs2[1, 0].plot(frames_centrados, vel_mun, color=color_p, linewidth=2.5)
        axs2[1, 0].set_title('Velocidad Muñeca / Lag (px/s)', fontsize=14)

        # Estabilidad Cabeza
        axs2[1, 1].plot(frames_centrados, est_cab, color='#2c3e50', linewidth=2.5)
        axs2[1, 1].set_title('Estabilidad Cabeza (Variación Vertical)', fontsize=14)

        # DIBUJAR LÍNEA ROJA EN LAS 4 GRÁFICAS Y PONER GRID
        for ax in axs2.flat:
            ax.axvline(x=0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Impacto')
            ax.set_xlabel('Frames (0 = Contacto)')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)

        plt.tight_layout(rect=[0, 0.03, 1, 0.96])
        ruta_grafica2 = os.path.join(dir_actual, f"Grafica_{nombre_base}_Amateur_Articular.png")
        plt.savefig(ruta_grafica2, dpi=300)
        plt.close(fig2)

    except Exception as e:
        print(f"❌ Error al generar gráficas del amateur: {e}")
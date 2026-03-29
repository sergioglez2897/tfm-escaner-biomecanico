import matplotlib.pyplot as plt
import csv
import os

# --- CONFIGURACIÓN ---
dir_actual = os.path.dirname(os.path.abspath(__file__))

jugadores = ["Alcaraz", "Sinner", "Djokovic", "Nadal"]

colores_jugador = {
    "Alcaraz": {"principal": "#3498db", "secundario": "#f1c40f"}, # Azul y Amarillo
    "Sinner": {"principal": "#e67e22", "secundario": "#c0392b"},  # Naranja y Rojo
    "Djokovic": {"principal": "#8e44ad", "secundario": "#2c3e50"}, # Morado y Azul Oscuro
    "Nadal": {"principal": "#27ae60", "secundario": "#d35400"}     # Verde y Arcilla
}

print("📊 Generando Informes Individuales PREMIUM para los 4 jugadores...")

for nombre in jugadores:
    csv_path = os.path.join(dir_actual, f"datos_{nombre}_premium.csv")
    
    if not os.path.exists(csv_path):
        print(f"⚠️ Aviso: No se encontró el archivo de {nombre}. Saltando...")
        continue

    frames, codo, r_hombros, r_caderas, sep_ch, rodilla, vel_mun, est_cab = [], [], [], [], [], [], [], []
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                frames.append(int(row['Frame']))
                codo.append(float(row['Angulo_Codo_Armado']))
                r_hombros.append(float(row['Rotacion_Hombros_Horizontal']))
                r_caderas.append(float(row['Rotacion_Caderas_Horizontal']))
                sep_ch.append(float(row['Separacion_CH_XFactor']))
                rodilla.append(float(row['Angulo_Rodilla_Apoyo']))
                vel_mun.append(float(row['Velocidad_Muneca_Lag']))
                est_cab.append(float(row['Estabilidad_Cabeza_VarV']))

        info_col = colores_jugador[nombre]
        plt.style.use('seaborn-v0_8-muted')

        # ==========================================
        # GRÁFICA 1: CADENA CINÉTICA (X-FACTOR)
        # ==========================================
        fig1, axs1 = plt.subplots(3, 1, figsize=(10, 14), sharex=True)
        fig1.suptitle(f'CADENA CINÉTICA: {nombre.upper()}', fontsize=20, fontweight='bold', color=info_col["principal"])

        axs1[0].plot(frames, r_hombros, color=info_col["principal"], linewidth=3)
        axs1[0].set_title('Rotación de Hombros (º)', fontsize=14)
        axs1[0].grid(True, alpha=0.3)

        axs1[1].plot(frames, r_caderas, color=info_col["secundario"], linewidth=3)
        axs1[1].set_title('Rotación de Caderas (º)', fontsize=14)
        axs1[1].grid(True, alpha=0.3)

        axs1[2].fill_between(frames, sep_ch, color='#e74c3c', alpha=0.2)
        axs1[2].plot(frames, sep_ch, color='#c0392b', linewidth=3)
        axs1[2].set_title('Separación Cadera-Hombros / X-Factor (º)', fontsize=14, fontweight='bold')
        axs1[2].set_xlabel('Tiempo (Frames)')
        axs1[2].grid(True, alpha=0.3)

        plt.tight_layout(rect=[0, 0.03, 1, 0.96])
        ruta_grafica1 = os.path.join(dir_actual, f"Grafica_{nombre}_1_Cinematica.png")
        plt.savefig(ruta_grafica1, dpi=300)
        plt.close(fig1)

        # ==========================================
        # GRÁFICA 2: ARTICULAR Y POTENCIA
        # ==========================================
        fig2, axs2 = plt.subplots(2, 2, figsize=(14, 10))
        fig2.suptitle(f'ARTICULACIONES Y POTENCIA: {nombre.upper()}', fontsize=20, fontweight='bold', color=info_col["principal"])

        axs2[0, 0].plot(frames, codo, color=info_col["principal"], linewidth=2.5)
        axs2[0, 0].set_title('Ángulo Codo (º)', fontsize=14)
        axs2[0, 0].grid(True, alpha=0.3)

        axs2[0, 1].plot(frames, rodilla, color=info_col["secundario"], linewidth=2.5)
        axs2[0, 1].set_title('Ángulo Rodilla Apoyo (º)', fontsize=14)
        axs2[0, 1].grid(True, alpha=0.3)

        axs2[1, 0].fill_between(frames, vel_mun, color=info_col["principal"], alpha=0.2)
        axs2[1, 0].plot(frames, vel_mun, color=info_col["principal"], linewidth=2.5)
        axs2[1, 0].set_title('Velocidad Muñeca / Lag (px/s)', fontsize=14)
        axs2[1, 0].set_xlabel('Frames')
        axs2[1, 0].grid(True, alpha=0.3)

        axs2[1, 1].plot(frames, est_cab, color='#2c3e50', linewidth=2.5)
        axs2[1, 1].set_title('Estabilidad Cabeza (Variación Vertical)', fontsize=14)
        axs2[1, 1].set_xlabel('Frames')
        axs2[1, 1].grid(True, alpha=0.3)

        plt.tight_layout(rect=[0, 0.03, 1, 0.96])
        ruta_grafica2 = os.path.join(dir_actual, f"Grafica_{nombre}_2_Articular.png")
        plt.savefig(ruta_grafica2, dpi=300)
        plt.close(fig2)

        print(f"✅ Gráficas generadas para {nombre}")

    except Exception as e:
        print(f"❌ Error al procesar a {nombre}: {e}")

print("🏆 ¡PROCESO COMPLETADO! Revisa tu carpeta TFM_TENIS.")
import matplotlib.pyplot as plt
import csv
import os

# --- CONFIGURACIÓN ---
dir_actual = os.path.dirname(os.path.abspath(__file__))

jugadores = {
    "Alcaraz": {"archivo": "datos_Alcaraz_premium.csv", "color": "#3498db"},
    "Sinner": {"archivo": "datos_Sinner_premium.csv", "color": "#e67e22"},
    "Djokovic": {"archivo": "datos_Djokovic_premium.csv", "color": "#8e44ad"},
    "Nadal": {"archivo": "datos_Nadal_premium.csv", "color": "#27ae60"}
}

output_graph = os.path.join(dir_actual, "SUPER_COMPARATIVA_PREMIUM.png")

print("📊 Generando la Super Comparativa Alineada al Impacto...")

# --- PREPARAR EL LIENZO GIGANTE ---
plt.style.use('seaborn-v0_8-muted')
# Matriz de 4x2 para alojar las 7 métricas
fig, axs = plt.subplots(4, 2, figsize=(20, 22))
fig.suptitle('ESTUDIO BIOMECÁNICO AVANZADO: COMPARATIVA ALINEADA AL IMPACTO (ÉLITE ATP)', fontsize=24, fontweight='bold', y=0.97)

# Ocultar el último gráfico (el hueco 8) porque solo tenemos 7 métricas
axs[3, 1].axis('off')

# --- LEER Y ALINEAR DATOS ---
for nombre, info in jugadores.items():
    ruta_csv = os.path.join(dir_actual, info["archivo"])
    
    if not os.path.exists(ruta_csv):
        print(f"⚠️ Aviso: No encuentro {info['archivo']}. Me lo salto.")
        continue
        
    f_orig, codo, r_hom, r_cad, sep_ch, rod, vel, est = [], [], [], [], [], [], [], []
    
    try:
        with open(ruta_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                f_orig.append(int(row['Frame']))
                codo.append(float(row['Angulo_Codo_Armado']))
                r_hom.append(float(row['Rotacion_Hombros_Horizontal']))
                r_cad.append(float(row['Rotacion_Caderas_Horizontal']))
                sep_ch.append(float(row['Separacion_CH_XFactor']))
                rod.append(float(row['Angulo_Rodilla_Apoyo']))
                vel.append(float(row['Velocidad_Muneca_Lag']))
                est.append(float(row['Estabilidad_Cabeza_VarV']))
                
        # --- EL TRUCO: ALINEACIÓN POR IMPACTO ---
        # Buscamos el pico de velocidad de la muñeca
        max_vel = max(vel)
        indice_impacto = vel.index(max_vel)
        frame_impacto = f_orig[indice_impacto]
        
        # Centramos todos los frames respecto al impacto (Frame 0)
        f_centrados = [f - frame_impacto for f in f_orig]
        
        # --- DIBUJAR LAS 7 LÍNEAS ---
        kwargs = {'label': nombre, 'color': info["color"], 'linewidth': 3, 'alpha': 0.85}
        
        # Fila 1: Potencia Pura
        axs[0, 0].plot(f_centrados, sep_ch, **kwargs) # X-Factor
        axs[0, 1].plot(f_centrados, vel, **kwargs)    # Velocidad Muñeca
        
        # Fila 2: Cadena Cinética (Rotaciones)
        axs[1, 0].plot(f_centrados, r_cad, **kwargs)  # Caderas
        axs[1, 1].plot(f_centrados, r_hom, **kwargs)  # Hombros
        
        # Fila 3: Articulaciones Clave
        axs[2, 0].plot(f_centrados, codo, **kwargs)   # Codo
        axs[2, 1].plot(f_centrados, rod, **kwargs)    # Rodilla
        
        # Fila 4: Estabilidad
        axs[3, 0].plot(f_centrados, est, **kwargs)    # Cabeza
        
        print(f"✅ {nombre}: Alineado al impacto (Frame original: {frame_impacto})")
        
    except Exception as e:
        print(f"❌ Error con {nombre}: {e}")

# --- CONFIGURACIÓN ESTÉTICA DE LOS 7 GRÁFICOS ---
configuraciones = [
    (axs[0,0], 'Separación Cadera-Hombros (X-Factor)', 'Grados (º)'),
    (axs[0,1], 'Velocidad de Muñeca (Lag)', 'Píxeles / seg'),
    (axs[1,0], 'Rotación de Caderas', 'Grados (º)'),
    (axs[1,1], 'Rotación de Hombros', 'Grados (º)'),
    (axs[2,0], 'Ángulo del Codo Armado', 'Grados (º)'),
    (axs[2,1], 'Flexoextensión Rodilla Delantera', 'Grados (º)'),
    (axs[3,0], 'Estabilidad de Cabeza (Variación Vertical)', 'Variación en Píxeles')
]

for ax, titulo, ylabel in configuraciones:
    ax.set_title(titulo, fontsize=16, fontweight='bold', pad=10)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_xlabel('Frames relativos al IMPACTO (0 = Contacto)', fontsize=12)
    
    # Línea vertical roja indicando el momento exacto del golpe
    ax.axvline(x=0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Punto de Impacto')
    
    ax.grid(True, linestyle='--', alpha=0.4)
    # Poner la leyenda solo una vez para no saturar, o en todas si prefieres (aquí en todas para claridad)
    ax.legend(fontsize=10, loc='best')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(output_graph, dpi=300)
print(f"🏆 ¡SUPER COMPARATIVA FINALIZADA! Imagen guardada en: {output_graph}")
plt.show()
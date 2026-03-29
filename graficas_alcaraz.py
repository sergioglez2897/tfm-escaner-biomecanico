import matplotlib.pyplot as plt
import csv
import os

# --- CONFIGURACIÓN DE RUTAS ---
dir_actual = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(dir_actual, "datos_Nadal.csv") 
output_graph = os.path.join(dir_actual, "graficas_biomecanicas_nadal.png")

frames = []
codo = []
hombro = []
rodilla = []
velocidad = []

print(f"📈 Generando gráficas individuales para Nadal desde: {csv_path}...")

try:
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            frames.append(int(row['Frame']))
            codo.append(float(row['Codo']))
            hombro.append(float(row['Hombro']))
            rodilla.append(float(row['Rodilla']))
            velocidad.append(float(row['Velocidad_Muñeca']))

    # Configuración estética (Tonos Nadal: Verdes y Arcilla)
    plt.style.use('seaborn-v0_8-muted') 
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('INFORME BIOMECÁNICO INDIVIDUAL: RAFAEL NADAL', fontsize=20, fontweight='bold', color='#27ae60')

    # 1. CODO
    axs[0, 0].plot(frames, codo, color='#2ecc71', linewidth=2.5)
    axs[0, 0].set_title('Ángulo del Codo (Grados)', fontsize=14)
    axs[0, 0].set_ylabel('Grados (º)')
    axs[0, 0].grid(True, alpha=0.3)

    # 2. HOMBRO
    axs[0, 1].plot(frames, hombro, color='#27ae60', linewidth=2.5)
    axs[0, 1].set_title('Ángulo del Hombro (Grados)', fontsize=14)
    axs[0, 1].grid(True, alpha=0.3)

    # 3. RODILLA
    axs[1, 0].plot(frames, rodilla, color='#d35400', linewidth=2.5) # Color arcilla
    axs[1, 0].set_title('Ángulo de la Rodilla (Grados)', fontsize=14)
    axs[1, 0].set_xlabel('Tiempo (Frames)')
    axs[1, 0].set_ylabel('Grados (º)')
    axs[1, 0].grid(True, alpha=0.3)

    # 4. VELOCIDAD MUÑECA
    axs[1, 1].fill_between(frames, velocidad, color='#f39c12', alpha=0.3)
    axs[1, 1].plot(frames, velocidad, color='#e67e22', linewidth=2.5)
    axs[1, 1].set_title('Velocidad de la Muñeca (Aceleración)', fontsize=14)
    axs[1, 1].set_xlabel('Tiempo (Frames)')
    axs[1, 1].set_ylabel('px/s')
    axs[1, 1].grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Guardar imagen
    plt.savefig(output_graph, dpi=300)
    print(f"✅ ¡Gráficas de Nadal guardadas! --> {output_graph}")
    
    plt.show()

except FileNotFoundError:
    print(f"❌ ERROR: No encuentro el archivo 'datos_Nadal.csv'.")
    print("Asegúrate de ejecutar primero el análisis del vídeo de Nadal.")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
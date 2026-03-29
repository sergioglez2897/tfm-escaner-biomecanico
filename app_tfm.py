import streamlit as st
import os
import pandas as pd
import motor_ia            
import graficas_amateur   

# --- CONFIGURACIÓN GENERAL ---
st.set_page_config(page_title="TFM Biomecánica Sergio", page_icon="🎾", layout="wide")
dir_actual = os.path.dirname(os.path.abspath(__file__))

# --- CONSTANTES DE LA ÉLITE ---
ELITE_X_FACTOR = 48.0    
ELITE_CODO = 105.0       
ELITE_RODILLA = 135.0    
ELITE_HOMBROS = 110.0    
ELITE_CABEZA = 5.0       

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .titulo-pro { background: -webkit-linear-gradient(45deg, #1e3c72, #2a5298); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3em; font-weight: 900; text-align: center; }
    div[data-testid="metric-container"] { background-color: white; border: 1px solid #e0e6ed; border-radius: 12px; padding: 15px; box-shadow: 2px 4px 12px rgba(0,0,0,0.04); }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3254/3254099.png", width=80)
    st.markdown("## TFM Biomecánica ATP")
    st.markdown("**Autor:** Sergio")

st.markdown('<p class="titulo-pro">🎾 Escáner Biomecánico ATP</p>', unsafe_allow_html=True)

# --- MEMORIA DE LA APP ---
if 'analisis_ok' not in st.session_state: st.session_state.analisis_ok = False
if 'video_actual' not in st.session_state: st.session_state.video_actual = ""

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
metrica_1 = col_m1.empty()
metrica_2 = col_m2.empty()
metrica_3 = col_m3.empty()
metrica_4 = col_m4.empty()

tab1, tab2 = st.tabs(["📊 PATRÓN ORO (La Élite)", "🎯 TU ENTRENADOR VIRTUAL (Amateur)"])

# ==========================================
# PESTAÑA 1: EL PATRÓN ORO (COMPARADOR DINÁMICO)
# ==========================================
with tab1:
    st.markdown("### 🏆 La Super Comparativa (Alineada al Impacto)")
    st.markdown("El **Patrón Oro** se ha extraído cruzando las constantes biomecánicas de los cuatro dominadores del circuito ATP. A continuación, puedes comparar cara a cara su ejecución técnica, sincronizada exactamente en el 'Frame 0' (momento del impacto).")
    
    ruta_super = os.path.join(dir_actual, "SUPER_COMPARATIVA_PREMIUM.png")
    if os.path.exists(ruta_super): st.image(ruta_super, use_container_width=True)

    st.divider()
    st.markdown("### ⚔️ Comparador Biomecánico Personalizado")
    
    col_sel1, col_sel2 = st.columns(2)
    jugador_A = col_sel1.selectbox("Jugador 1:", ["Alcaraz", "Sinner", "Djokovic", "Nadal"], index=0, key="j1")
    jugador_B = col_sel2.selectbox("Jugador 2:", ["Alcaraz", "Sinner", "Djokovic", "Nadal"], index=1, key="j2")
    
    col_A, col_B = st.columns(2)
    
    # --- JUGADOR A (Izquierda) ---
    with col_A:
        st.markdown(f"<h4 style='text-align: center; color: #1e3c72;'>Análisis: {jugador_A}</h4>", unsafe_allow_html=True)
        
        # 1. Vídeo
        ruta_vid_A = os.path.join(dir_actual, f"Analisis_{jugador_A}_Premium.mp4")
        if os.path.exists(ruta_vid_A):
            st.video(ruta_vid_A)
        else:
            st.warning(f"Vídeo no encontrado: Analisis_{jugador_A}_Premium.mp4")
            
        # 2. Selector de Gráficas A
        ver_graf_A = st.multiselect(f"¿Qué gráficas de {jugador_A} quieres ver?", 
                                    ["Cinemática", "Articular"], 
                                    default=["Cinemática", "Articular"], key="sel_A")
        
        if "Cinemática" in ver_graf_A:
            ruta_cin_A = os.path.join(dir_actual, f"Grafica_{jugador_A}_1_Cinematica.png")
            if os.path.exists(ruta_cin_A): st.image(ruta_cin_A, use_container_width=True)
            else: st.info(f"Falta archivo: {ruta_cin_A}")
            
        if "Articular" in ver_graf_A:
            ruta_art_A = os.path.join(dir_actual, f"Grafica_{jugador_A}_2_Articular.png")
            if os.path.exists(ruta_art_A): st.image(ruta_art_A, use_container_width=True)
            else: st.info(f"Falta archivo: {ruta_art_A}")

    # --- JUGADOR B (Derecha) ---
    with col_B:
        st.markdown(f"<h4 style='text-align: center; color: #1e3c72;'>Análisis: {jugador_B}</h4>", unsafe_allow_html=True)
        
        # 1. Vídeo
        ruta_vid_B = os.path.join(dir_actual, f"Analisis_{jugador_B}_Premium.mp4")
        if os.path.exists(ruta_vid_B):
            st.video(ruta_vid_B)
        else:
            st.warning(f"Vídeo no encontrado: Analisis_{jugador_B}_Premium.mp4")
            
        # 2. Selector de Gráficas B
        ver_graf_B = st.multiselect(f"¿Qué gráficas de {jugador_B} quieres ver?", 
                                    ["Cinemática", "Articular"], 
                                    default=["Cinemática", "Articular"], key="sel_B")
        
        if "Cinemática" in ver_graf_B:
            ruta_cin_B = os.path.join(dir_actual, f"Grafica_{jugador_B}_1_Cinematica.png")
            if os.path.exists(ruta_cin_B): st.image(ruta_cin_B, use_container_width=True)
            else: st.info(f"Falta archivo: {ruta_cin_B}")
            
        if "Articular" in ver_graf_B:
            ruta_art_B = os.path.join(dir_actual, f"Grafica_{jugador_B}_2_Articular.png")
            if os.path.exists(ruta_art_B): st.image(ruta_art_B, use_container_width=True)
            else: st.info(f"Falta archivo: {ruta_art_B}")

# ==========================================
# PESTAÑA 2: EL ANALIZADOR AMATEUR (COMPLETA)
# ==========================================
with tab2:
    col_izq, col_der = st.columns([1, 2])
    
    with col_izq:
        st.markdown("### 1. Sube tu vídeo")
        archivo_video = st.file_uploader("Selecciona tu vídeo (.mp4)", type=['mp4', 'mov'])
        rotacion_elegida = st.selectbox("¿El vídeo grabado sale girado o al revés?", 
                                      ["Ninguna", "Rotar 90º a la Derecha ↻", "Rotar 90º a la Izquierda ↺", "Rotar 180º (Al revés)"])
        
        if archivo_video is not None and archivo_video.name != st.session_state.video_actual:
            st.session_state.analisis_ok = False
            st.session_state.video_actual = archivo_video.name
        
        if archivo_video is not None:
            if st.button("🚀 INICIAR ESCÁNER BIOMECÁNICO", type="primary", use_container_width=True):
                with st.spinner('Poniendo la lupa a tu técnica...'):
                    ruta_temp = os.path.join(dir_actual, "temp_amateur.mp4")
                    with open(ruta_temp, "wb") as f: f.write(archivo_video.read())
                    
                    nombre_base = archivo_video.name.split('.')[0]
                    ruta_out = os.path.join(dir_actual, f"Analisis_{nombre_base}.mp4")
                    ruta_csv = os.path.join(dir_actual, f"Datos_{nombre_base}.csv")
                    
                    exito = motor_ia.procesar_video_amateur(ruta_temp, ruta_out, ruta_csv, rotacion_elegida)
                    if exito:
                        graficas_amateur.generar_graficas_amateur(nombre_base)
                        st.session_state.analisis_ok = True  

    with col_der:
        if archivo_video is not None: st.video(archivo_video)
        else: st.info("Sube tu archivo para previsualizarlo aquí.")
            
    # --- ZONA DE RESULTADOS EXTENSOS ---
    if st.session_state.analisis_ok and archivo_video is not None:
        st.divider()
        nombre_base = st.session_state.video_actual.split('.')[0]
        ruta_csv = os.path.join(dir_actual, f"Datos_{nombre_base}.csv")
        
        try:
            df = pd.read_csv(ruta_csv)
            max_xf = df['Separacion_CH_XFactor'].max()
            max_hom = df['Rotacion_Hombros_Horizontal'].max()
            max_cad = df['Rotacion_Caderas_Horizontal'].max()
            med_codo = df.iloc[len(df)//3 : len(df)//2]['Angulo_Codo_Armado'].mean()
            min_rodilla = df['Angulo_Rodilla_Apoyo'].min() 
            max_lag = df['Velocidad_Muneca_Lag'].max()
            med_est = df['Estabilidad_Cabeza_VarV'].mean()

            metrica_1.metric("Efecto Muelle (X-Factor)", f"{int(max_xf)}º", f"Alcaraz: ~{int(ELITE_X_FACTOR)}º")
            metrica_2.metric("Latigazo Final", f"{int(max_lag)} px/s", "Aceleración")
            metrica_3.metric("Postura del Brazo", f"{int(med_codo)}º", f"Nadal: ~{int(ELITE_CODO)}º")
            metrica_4.metric("Quietud de Cabeza", f"{int(med_est)} px", f"Federer: <{int(ELITE_CABEZA)}px")

            st.markdown("### 🗣️ Diagnóstico Biomecánico Profundo")
            
            # 1. HOMBROS Y CADERAS (PREPARACIÓN)
            with st.expander("1. Fase de Preparación (Unit Turn) - Caderas y Hombros", expanded=True):
                st.markdown(f"**Tus datos exactos:** Has rotado los hombros **{int(max_hom)}º** y las caderas **{int(max_cad)}º** en la fase de armado.")
                st.markdown("""
                **Análisis del movimiento:** El golpe de derecha moderno no se prepara echando el brazo hacia atrás, sino realizando un 'Unit Turn' (giro en bloque). Al girar el pecho hasta ponerlo perpendicular a la red (superando los 100º), creas una pista de aterrizaje larguísima para que tu raqueta pueda coger velocidad antes de impactar la bola. Si no giras lo suficiente, el recorrido de tu raqueta será muy corto y tu golpe será débil.
                """)
                if max_hom >= 100: 
                    st.success("✅ **Diagnóstico:** Tienes una preparación de libro. Al enseñar tu espalda a la red, te aseguras de tener el espacio y el tiempo suficiente para acelerar el brazo con soltura.")
                else: 
                    st.error(f"⚠️ **Diagnóstico:** Tu preparación es demasiado frontal. Te faltan unos {int(100 - max_hom)}º de giro de hombros. Ahora mismo estás usando solo la articulación de tu hombro para llevar la raqueta atrás, lo cual limita muchísimo tu potencia y puede causarte molestias a largo plazo.")

            # 2. X-FACTOR Y ESTILO DE JUEGO
            with st.expander("2. El Motor de Potencia (X-Factor y Estilo de Juego)", expanded=True):
                st.markdown(f"**Tu dato exacto:** Has logrado un máximo de **{int(max_xf)}º** de separación entre cadera y hombros.")
                st.markdown(f"**El patrón de Élite:** Existen dos grandes estilos. El clásico (Alcaraz, Sinner) busca **45º-55º** de separación. El moderno/semi-abierto (Kyrgios, Medvedev) ronda los **20º-30º**, compensando con una velocidad de brazo extrema.")
                st.markdown("""
                **Análisis del movimiento:** En la biomecánica avanzada, el X-Factor no es una regla estricta de 'más es siempre mejor', sino un indicador de **tu estilo de juego personal**. Puedes generar potencia de dos formas totalmente válidas: retorciendo tu abdomen como un muelle (alta torsión), o adoptando una posición más abierta para girar en bloque y catapultar el brazo como un látigo (baja torsión pero altísima velocidad de muñeca).
                """)
                
                if max_xf >= 35: 
                    st.success("🎾 **Tu Perfil: Estilo Torsión (Clásico).** ¡Excelente ejecución! Perteneces al grupo de jugadores que basan su fuerza en la separación tronco-pelvis. Sabes retorcer tu cuerpo para generar la famosa 'Heavy Ball' (bola pesada y con mucho peso) sin forzar las articulaciones del brazo. Es un estilo tremendamente sólido y potente.")
                else: 
                    if max_lag >= 130:
                        st.success("🔥 **Tu Perfil: Estilo Látigo (Moderno / Semi-Open).** ¡Gran nivel técnico! Tu separación de tronco es menor, lo que indica que usas una posición de pies más abierta y adecuada para un tenis rápido. No necesitas retorcerte tanto porque confías en un giro en bloque y en una **aceleración de muñeca fulminante**. Es una biomecánica ideal para restar o atacar bolas rápidas, generando un tiro muy vivo y agresivo.")
                    else:
                        st.warning("⚠️ **Diagnóstico de mejora:** Tu X-Factor es bajito y tu latigazo de muñeca también. Esto significa que estás empujando la bola solo con la fuerza del hombro. Para ganar potencia real, tienes que elegir un camino: o giras más los hombros hacia atrás para crear 'efecto muelle', o relajas más la muñeca para lograr un buen latigazo final.")

            # 3. VELOCIDAD Y LAG DE MUÑECA
            with st.expander("3. Aceleración y Relajación (Lag de Muñeca)", expanded=True):
                st.markdown(f"**Tu dato exacto:** El pico máximo de velocidad de tu muñeca es de **{int(max_lag)} píxeles/segundo**.")
                st.markdown("""
                **Análisis del movimiento:** En el tenis no gana quien hace más fuerza con el antebrazo, gana quien relaja mejor la muñeca. El 'Lag' (retraso de la raqueta) sucede cuando el tapón de tu raqueta apunta hacia la bola justo antes de pegar. Al frenar en seco la rotación de tus hombros, toda esa energía acumulada se transfiere a la raqueta, que sale disparada hacia adelante multiplicando su velocidad como el chasquido de un látigo.
                """)
                st.info("🔍 **Diagnóstico:** Mira la gráfica 2 (abajo a la izquierda). Si tu pico de velocidad ocurre EXACTAMENTE en la línea roja del impacto, significa que tu latigazo es perfecto y estás impactando la bola en el momento de máxima aceleración. Si el pico ocurre antes, estás frenando el brazo por tensión o miedo a fallar.")

            # 4. RODILLA (FUERZAS DEL SUELO)
            with st.expander("4. Transferencia de Peso (Flexión de Rodilla)", expanded=True):
                st.markdown(f"**Tu dato exacto:** Has flexionado la rodilla delantera hasta los **{int(min_rodilla)}º** (180º significa estar totalmente de pie).")
                st.markdown(f"**El patrón de Élite:** Los profesionales suelen bajar hasta los **130º-140º** para cargar peso.")
                st.markdown("""
                **Análisis del movimiento:** La cadena cinética nace en el suelo. Al flexionar las rodillas, 'cargas' energía contra el piso (Fuerzas de Reacción del Suelo). Al iniciar el golpe, empujas el suelo hacia abajo y esa energía sube por tus piernas, pasa a tus caderas, luego al tronco y finalmente al brazo.
                """)
                if min_rodilla <= 145: 
                    st.success("✅ **Diagnóstico:** Tienes una base muy sólida. Estás bajando el centro de gravedad correctamente, lo que te permite absorber la bola del rival e inyectar fuerza extra usando los grandes músculos de tus piernas (cuádriceps y glúteos).")
                else: 
                    st.error(f"⚠️ **Diagnóstico:** Estás golpeando muy erguido. Te faltan unos {int(min_rodilla - ELITE_RODILLA)}º de flexión. Si golpeas 'de pie', tu centro de gravedad está muy alto, te desequilibras fácil y las piernas no aportan absolutamente nada de potencia al golpe.")

            # 5. CODO
            with st.expander("5. Palanca y Protección (Estructura del Codo)", expanded=True):
                st.markdown(f"**Tu dato exacto:** En el momento de impacto, tu codo dibuja un ángulo de **{int(med_codo)}º**.")
                st.markdown(f"**El patrón de Élite:** La técnica moderna (Nadal, Djokovic) se basa en el 'Doble Doblez', manteniendo el codo entre **90º y 115º**.")
                st.markdown("""
                **Análisis del movimiento:** La distancia al punto de contacto es vital. Si pegas con el brazo totalmente recto (180º), alejas mucho la masa de tu cuerpo de la bola y sometes a la articulación del codo a un estrés altísimo que termina en lesiones. Si pegas muy encogido (< 80º), te quedas sin palanca (momento de inercia) y la raqueta no corre.
                """)
                if 85 <= med_codo <= 125: 
                    st.success("✅ **Diagnóstico:** Tienes una distancia de impacto perfecta. Al mantener una ligera flexión en L, proteges tus tendones, mejoras tu control y permites que el antebrazo pueda rotar (pronación) de forma natural para generar efecto (Topspin).")
                elif med_codo > 125: 
                    st.warning(f"⚠️ **Diagnóstico:** Pegas demasiado lejos del cuerpo. Tu brazo está casi recto ({int(med_codo)}º). Esto provoca fatiga y te resta maniobrabilidad ante bolas rápidas. Intenta dejar entrar la bola un poco más.")
                else:
                    st.error(f"⚠️ **Diagnóstico:** Pegas 'comiéndote' la bola. Tu ángulo es muy agudo ({int(med_codo)}º). Ajusta los pasos cortos antes de pegar para separarte de la trayectoria de la bola.")

            # 6. ESTABILIDAD DE CABEZA
            with st.expander("6. El Eje de Rotación (Quietud de la Cabeza)", expanded=True):
                st.markdown(f"**Tu dato exacto:** Tu cabeza ha sufrido una variación vertical de **{int(med_est)} píxeles** durante el swing.")
                st.markdown(f"**El patrón de Élite:** Roger Federer fijó el estándar mundial con variaciones casi nulas (**< 5 píxeles**).")
                st.markdown("""
                **Análisis del movimiento:** La cabeza de un adulto pesa entre 4 y 5 kg. Si mueves la cabeza bruscamente hacia arriba o hacia los lados mientras golpeas (normalmente por la ansiedad de ver adónde va la bola), el peso de la cabeza arrastra los hombros, tu eje de rotación se rompe, y terminas pegando cañas o descentrando el impacto.
                """)
                if med_est <= 15: 
                    st.success("✅ **Diagnóstico:** Tienes una disciplina visual excelente. Al mantener la cabeza anclada y quieta en la zona de contacto, aislas el tren superior y te aseguras de golpear con el punto dulce de la raqueta sistemáticamente.")
                else: 
                    st.error(f"❌ **Diagnóstico:** Te mueves demasiado pronto. Tu variación de {int(med_est)} px indica que estás levantando la vista o tirando la cabeza hacia atrás. Regla de oro: oblígate a mirar las cuerdas de tu raqueta durante un segundo entero DESPUÉS de haber golpeado la bola.")

        except Exception as e: st.error(f"Error procesando CSV: {e}")

        # --- GRÁFICAS DEL AMATEUR ---
        r_c = os.path.join(dir_actual, f"Grafica_{nombre_base}_Amateur_Cinematica.png")
        r_a = os.path.join(dir_actual, f"Grafica_{nombre_base}_Amateur_Articular.png")
        if os.path.exists(r_c) and os.path.exists(r_a):
            st.markdown("### 📉 Tus Gráficas de Rendimiento Biomecánico")
            c1, c2 = st.columns(2)
            c1.image(r_c, use_container_width=True)
            c2.image(r_a, use_container_width=True)
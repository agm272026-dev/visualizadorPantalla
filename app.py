import streamlit as st
import time
import os

# 1. Configuración de pantalla completa
st.set_page_config(page_title="Visualizador Concordia", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Avanzado para Fondo Negro, Calendario Verde y Flyer a Pantalla Completa
st.markdown("""
    <style>
    .stApp, .main, .block-container { background-color: #000000 !important; }
    .block-container { padding: 0rem !important; }
    header, footer { visibility: hidden; }

    /* Estilo del Calendario: Verde Brillante */
    .dark-calendar {
        filter: invert(0.9) hue-rotate(90deg) brightness(1.7) contrast(1.4);
        background-color: #000000;
        display: block;
    }
    
    /* * SOLUCIÓN DEL ESPACIO MUERTO:
     * Apuntamos directamente al contenedor de imagen nativo de Streamlit 
     */
    [data-testid="stImage"] {
        height: 100vh !important; /* Fuerza al contenedor a medir el 100% del alto de la ventana */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    [data-testid="stImage"] img {
        height: 100vh !important; 
        width: 100% !important;
        /* IMPORTANTE: 
           Usa 'contain' si quieres ver el flyer completo sin que se recorte (pueden quedar bandas negras a los lados).
           Usa 'cover' si prefieres que la imagen se amplíe y recorte para llenar todo el ancho disponible.
        */
        object-fit: contain; 
    }
    
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Ajuste de columnas: Le damos más ancho al flyer (ej. 1 parte flyer, 2 partes calendario)
# Puedes jugar con estos números, ej: [1, 1] para mitad y mitad, o [2, 3].
col_flyers, col_calendar = st.columns([1, 2])

with col_flyers:
    placeholder = st.empty()
    ruta_flyers = "flyers"
    if not os.path.exists(ruta_flyers): os.makedirs(ruta_flyers)
    
    # El loop de flyers
    def run_flyers():
        while True:
            lista_flyers = [f for f in os.listdir(ruta_flyers) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if lista_flyers:
                for imagen in lista_flyers:
                    with placeholder.container():
                        # Ya no necesitamos el div extra, el CSS global se encarga
                        st.image(os.path.join(ruta_flyers, imagen), width="stretch")
                    time.sleep(10)
            else:
                placeholder.info("Cargando flyers...")
                time.sleep(5)

with col_calendar:
    # URL con parámetros para ocultar zona horaria y títulos
    google_cal_url = "https://calendar.google.com/calendar/embed?src=subsecretariadedeportescdia%40gmail.com&ctz=America%2FArgentina%2FCordoba&showTitle=0&showNav=1&showDate=1&showPrint=0&showTabs=0&showCalendars=0&showTz=0"
    
    st.markdown(f"""
        <div style="background-color: #000000; width: 100%; height: 100vh; overflow: hidden;">
            <iframe src="{google_cal_url}" class="dark-calendar" 
            style="width: 100%; height: 110vh; border: none; margin-top: -50px;" 
            frameborder="0" scrolling="no"></iframe>
        </div>
    """, unsafe_allow_html=True)

run_flyers()

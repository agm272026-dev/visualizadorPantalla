import streamlit as st
import time
import os

st.set_page_config(page_title="Visualizador Concordia", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp, .main, .block-container { background-color: #000000 !important; }
    .block-container { padding: 0rem !important; }
    header, footer { visibility: hidden; }
    .dark-calendar {
        filter: invert(0.9) hue-rotate(-290deg) brightness(1.7) contrast(1.4);
        background-color: #000000;
        display: block;
    }
    [data-testid="stImage"] {
        height: 100vh !important;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    [data-testid="stImage"] img {
        height: 100vh !important; 
        width: 100% !important;
        object-fit: contain; 
    }
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

col_flyers, col_calendar = st.columns([1, 1.8])

flyer_placeholder = col_flyers.empty()
cal_placeholder = col_calendar.empty()

ruta_flyers = "flyers"
if not os.path.exists(ruta_flyers):
    os.makedirs(ruta_flyers)

google_cal_url = "https://calendar.google.com/calendar/embed?src=subsecretariadedeportescdia%40gmail.com&ctz=America%2FArgentina%2FCordoba&showTitle=0&showNav=1&showDate=1&showPrint=0&showTabs=0&showCalendars=0&showTz=0"

def render_calendar():
    """Genera el iframe del calendario con timestamp para evitar caché."""
    timestamp = int(time.time())
    refresh_url = f"{google_cal_url}&nocache={timestamp}"
    cal_html = f"""
        <div style="background-color: #000000; width: 108%; height: 100vh; overflow: hidden; margin-left: -95px;">
            <iframe src="{refresh_url}" class="dark-calendar" 
            style="width: 101%; height: 100vh; border: none; margin-top: -50px;" 
            frameborder="0" scrolling="no"></iframe>
        </div>
    """
    cal_placeholder.markdown(cal_html, unsafe_allow_html=True)

def main_loop():
    flyer_index = 0
    ciclo = 0          # cuenta cuántos ciclos de 10s pasaron
    CICLOS_CALENDARIO = 6   # refrescar calendario cada 3 ciclos = 60 segundos

    while True:
        # --- CALENDARIO: solo cada 30 segundos ---
        if ciclo % CICLOS_CALENDARIO == 0:
            render_calendar()

        # --- FLYER: cada 10 segundos siempre ---
        lista_flyers = sorted([
            f for f in os.listdir(ruta_flyers)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ])

        if lista_flyers:
            if flyer_index >= len(lista_flyers):
                flyer_index = 0

            imagen_actual = lista_flyers[flyer_index]
            with flyer_placeholder.container():
                st.image(os.path.join(ruta_flyers, imagen_actual), width="stretch")

            flyer_index += 1
        else:
            flyer_placeholder.info("Cargando flyers...")

        ciclo += 1
        time.sleep(10)

main_loop()

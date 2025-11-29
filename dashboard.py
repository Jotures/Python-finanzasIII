import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Finanzas en Vivo", page_icon="📡", layout="wide")

# 2. FUNCIÓN DE CONEXIÓN SEGURA
# Usamos ttl=60 para que los datos se actualicen cada 60 segundos si hay cambios
@st.cache_data(ttl=60)
def cargar_datos_gsheets():
    # Definimos el alcance de los permisos
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # LÓGICA HÍBRIDA:
    # Intento A: Buscar archivo local (Tu PC)
    if os.path.exists("credentials.json"):
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    # Intento B: Buscar secretos en la nube (Streamlit Cloud)
# Intento B: Buscar secretos en la nube (Formato JSON String)
    elif "service_account_json" in st.secrets:
        creds_dict = json.loads(st.secrets["service_account_json"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        st.error("❌ No se encontraron credenciales (ni locales ni en secretos).")
        return pd.DataFrame() # Retorna vacío si falla

    # Conectar y bajar datos
    client = gspread.authorize(creds)
    sheet = client.open("Finanzas Personales DB").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

try:
    # Cargar datos
    df = cargar_datos_gsheets()

    # --- VERIFICACIÓN DE DATOS VACÍOS ---
    if df.empty:
        st.warning("⚠️ La hoja de cálculo está vacía o no se pudo leer.")
        st.stop()

    # --- SIDEBAR ---
    st.sidebar.title("Filtros en Vivo")
    
    # Filtro de Categoría (Leemos las categorías reales que escribiste en Sheets)
    if 'categoria' in df.columns:
        cats = ['Todas'] + list(df['categoria'].unique())
        cat_select = st.sidebar.selectbox("Categoría:", cats)
        
        if cat_select != 'Todas':
            df = df[df['categoria'] == cat_select]

    # --- DASHBOARD ---
    st.title("📡 Finanzas Personales (Google Sheets)")
    st.caption("Los datos se actualizan desde tu hoja de cálculo.")
    st.markdown("---")

    # KPIs
    # Aseguramos que la columna monto sea numérica
    df['monto'] = pd.to_numeric(df['monto'], errors='coerce').fillna(0)
    
    # Aquí asumo que tus datos en Sheets son TODOS gastos positivos.
    # Si usas negativos, avísame. Por ahora sumamos todo como 'Gasto Total'.
    total_gastado = df['monto'].sum()
    movimientos = len(df)

    c1, c2 = st.columns(2)
    c1.metric("Gasto Total Acumulado", f"S/ {total_gastado:,.2f}")
    c2.metric("Movimientos Registrados", movimientos)

    st.markdown("---")

    # GRÁFICOS
    col1, col2 = st.columns([2,1])
    
    with col1:
        st.subheader("Gasto por Categoría")
        if not df.empty:
            fig_bar = px.bar(df, x='categoria', y='monto', color='categoria')
            st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Últimos Registros")
        # Mostramos las columnas más importantes
        cols_ver = ['fecha', 'descripcion', 'monto']
        # Filtramos solo las columnas que existen
        cols_final = [c for c in cols_ver if c in df.columns]
        st.dataframe(df[cols_final], hide_index=True)

except Exception as e:
    st.error(f"Ocurrió un error: {e}")
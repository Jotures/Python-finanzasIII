import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from datetime import date

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Finanzas 360", page_icon="💳", layout="wide")

# 2. CONEXIÓN AL ROBOT (Backend)
def conectar_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    if os.path.exists("credentials.json"):
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    elif "service_account_json" in st.secrets:
        creds_dict = json.loads(st.secrets["service_account_json"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        st.error("❌ Falta configuración de credenciales.")
        return None
    
    client = gspread.authorize(creds)
    # Abre la hoja y selecciona la primera pestaña
    return client.open("Finanzas Personales DB").sheet1

# 3. LEER DATOS (Cache para rapidez)
@st.cache_data(ttl=10) # Se actualiza cada 10 seg
def cargar_datos():
    sheet = conectar_google_sheets()
    if sheet:
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    return pd.DataFrame()

# 4. GUARDAR DATOS (Nueva función de escritura)
def guardar_gasto(fecha, descripcion, categoria, monto):
    sheet = conectar_google_sheets()
    if sheet:
        # append_row escribe una nueva fila al final
        sheet.append_row([str(fecha), descripcion, categoria, monto])
        # Limpiamos el caché para que el cambio se vea inmediato
        st.cache_data.clear()

try:
    # --- BARRA LATERAL: FORMULARIO DE INGRESO ---
    st.sidebar.title("➕ Nuevo Movimiento")
    
    with st.sidebar.form(key="form_gasto"):
        # Inputs del usuario
        fecha_input = st.date_input("Fecha", date.today())
        desc_input = st.text_input("Descripción (Ej: Taxi)")
        
        # Categorías predefinidas (puedes cambiarlas)
        cats_disponibles = ['Comida', 'Transporte', 'Alquiler', 'Entretenimiento', 'Servicios', 'Salud', 'Otros']
        cat_input = st.selectbox("Categoría", cats_disponibles)
        
        monto_input = st.number_input("Monto (S/)", min_value=0.01, format="%.2f")
        
        # Botón de envío
        submit_button = st.form_submit_button(label="💾 Guardar Gasto")

    # Lógica al presionar el botón
    if submit_button:
        if desc_input and monto_input > 0:
            with st.spinner("Enviando a la nube..."):
                guardar_gasto(fecha_input, desc_input, cat_input, monto_input)
            st.success("✅ ¡Guardado!")
            # Recargar la app para ver el cambio
            st.rerun()
        else:
            st.sidebar.error("⚠️ Faltan datos (Descripción o Monto).")

    st.sidebar.markdown("---")

    # --- CUERPO PRINCIPAL: DASHBOARD ---
    df = cargar_datos()

    if df.empty:
        st.info("👋 Tu hoja de cálculo está vacía. ¡Usa el formulario de la izquierda para agregar tu primer gasto!")
        st.stop()

    # Título
    st.title("📊 Mi Billetera en Vivo")

    # Filtros de visualización
    st.sidebar.header("🔍 Filtros")
    filtro_cat = st.sidebar.selectbox("Filtrar vista:", ["Todas"] + list(df['categoria'].unique()))
    
    df_view = df.copy()
    if filtro_cat != "Todas":
        df_view = df[df['categoria'] == filtro_cat]

    # KPIs
    # Convertir monto a números por si acaso
    df_view['monto'] = pd.to_numeric(df_view['monto'], errors='coerce').fillna(0)
    
    total = df_view['monto'].sum()
    promedio = df_view['monto'].mean()

    c1, c2 = st.columns(2)
    c1.metric("Total Gastado", f"S/ {total:,.2f}")
    c2.metric("Gasto Promedio", f"S/ {promedio:,.2f}")

    # Gráficos y Tabla
    col_graf, col_tabla = st.columns([2, 1])
    
    with col_graf:
        st.subheader("Desglose")
        fig = px.pie(df_view, names='categoria', values='monto', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
        
    with col_tabla:
        st.subheader("Últimos Registros")
        # Mostramos los últimos 5 (tail) e invertimos el orden
        st.dataframe(df_view.tail(10).iloc[::-1], hide_index=True)

except Exception as e:
    st.error(f"Algo salió mal: {e}")
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Finanzas Personales 2025", page_icon="💰", layout="wide")

# 2. CARGAR DATOS (Cache para velocidad)
@st.cache_data
def cargar_datos():
    # Leemos el Excel que generamos en el paso anterior
    df = pd.read_excel('EstadoCuenta_2025.xlsx')
    return df

try:
    df = cargar_datos()

    # --- BARRA LATERAL (SIDEBAR) ---
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2830/2830289.png", width=100)
    st.sidebar.title("Filtros")
    
    # Filtro: Tipo de Gasto (buscando en descripción)
    opciones = ['Todos', 'Supermercado', 'Grifo', 'Restaurante', 'Farmacia']
    filtro = st.sidebar.selectbox("Filtrar por categoría:", opciones)

    # Lógica de filtrado simple
    df_filtrado = df.copy()
    if filtro != 'Todos':
        df_filtrado = df[df['Descripción'].str.contains(filtro.upper())]

    # --- PÁGINA PRINCIPAL ---
    st.title("📊 Monitor de Finanzas Personales")
    st.markdown("---")

    # 3. KPIs (Indicadores)
    gastos = df_filtrado[df_filtrado['Importe'] < 0]['Importe'].abs().sum()
    ingresos = df_filtrado[df_filtrado['Importe'] > 0]['Importe'].sum()
    balance = ingresos - gastos

    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos", f"S/ {ingresos:,.2f}")
    c2.metric("Gastos", f"S/ {gastos:,.2f}", delta=-gastos, delta_color="inverse")
    c3.metric("Balance", f"S/ {balance:,.2f}")

    st.markdown("---")

    # 4. GRÁFICOS (Plotly)
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        st.subheader("Tendencia de Gastos")
        # Gráfico de línea temporal
        solo_gastos = df_filtrado[df_filtrado['Importe'] < 0].copy()
        solo_gastos['Importe'] = solo_gastos['Importe'].abs()
        solo_gastos = solo_gastos.sort_values('Fecha Operación')
        
        fig = px.area(solo_gastos, x='Fecha Operación', y='Importe', color_discrete_sequence=['#FF4B4B'])
        st.plotly_chart(fig, use_container_width=True)

    with col_der:
        st.subheader("Top Movimientos")
        st.dataframe(df_filtrado[['Fecha Operación', 'Descripción', 'Importe']], hide_index=True)

except Exception as e:
    st.error(f"⚠️ Error: {e}")
    st.info("Asegúrate de que el archivo 'EstadoCuenta_2025.xlsx' existe en la carpeta.")
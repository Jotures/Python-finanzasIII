import pandas as pd

print("📂 Abriendo libro de Excel...")
df = pd.read_excel('EstadoCuenta_2025.xlsx')

# --- PROCESAMIENTO ---
# 1. Filtrar solo gastos
gastos = df[df['Importe'] < 0].copy()
gastos['Importe'] = gastos['Importe'].abs() # Quitar signo negativo

# 2. Categorizar
def clasificar(texto):
    if 'SUPERMERCADO' in texto: return 'Comida 🛒'
    if 'GRIFO' in texto: return 'Transporte ⛽'
    if 'RESTAURANTE' in texto: return 'Salidas 🍔'
    if 'FARMACIA' in texto: return 'Salud 💊'
    return 'Otros 📦'

gastos['Categoria'] = gastos['Descripción'].apply(clasificar)

# 3. Crear Resumen (Tabla Dinámica)
resumen = gastos.groupby('Categoria')['Importe'].sum().sort_values(ascending=False).reset_index()

# --- EXPORTACIÓN A EXCEL ---
print("💾 Guardando reporte en 'Reporte_Final.xlsx'...")

# Usamos ExcelWriter para crear múltiples pestañas
with pd.ExcelWriter('Reporte_Final.xlsx') as writer:
    # Pestaña 1: El resumen
    resumen.to_excel(writer, sheet_name='Resumen Ejecutivo', index=False)
    
    # Pestaña 2: Los datos detallados
    gastos.to_excel(writer, sheet_name='Detalle de Gastos', index=False)

print("✅ ¡Éxito! Abre el archivo 'Reporte_Final.xlsx' para ver el resultado.")
import pandas as pd

print("📂 Abriendo libro de Excel...")

# 1. LEER EXCEL (La función clave es read_excel)
df = pd.read_excel('EstadoCuenta_2025.xlsx')

# Muestra las primeras 3 filas para ver qué tenemos
print("\n--- Vista previa de los datos ---")
print(df.head(3))

# 2. LIMPIEZA DE DATOS
# Filtramos solo lo que sea GASTO (menor a 0)
gastos = df[df['Importe'] < 0].copy()

# Convertimos a positivo para sumar mejor
gastos['Importe'] = gastos['Importe'].abs()

# 3. CATEGORIZACIÓN INTELIGENTE (Búsqueda de texto)
# Creamos una columna nueva 'Categoria' basada en la descripción
def clasificar(texto):
    if 'SUPERMERCADO' in texto: return 'Comida 🛒'
    if 'GRIFO' in texto: return 'Transporte ⛽'
    if 'RESTAURANTE' in texto: return 'Salidas 🍔'
    if 'FARMACIA' in texto: return 'Salud 💊'
    return 'Otros 📦'

# Aplicamos la función a cada fila
gastos['Categoria'] = gastos['Descripción'].apply(clasificar)

# 4. REPORTE FINAL
resumen = gastos.groupby('Categoria')['Importe'].sum().sort_values(ascending=False)

print("\n" + "="*40)
print("📊 REPORTE DE GASTOS BANCARIOS (EXCEL)")
print("="*40)
print(resumen)
print("-" * 40)
print(f"TOTAL GASTADO: S/ {gastos['Importe'].sum():,.2f}")
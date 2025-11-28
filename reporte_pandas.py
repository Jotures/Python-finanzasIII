import pandas as pd
import matplotlib.pyplot as plt

print("📂 Procesando datos...")
df = pd.read_csv('mis_gastos.csv')

# Agrupar datos
reporte = df.groupby('Categoria')['Monto'].sum().sort_values(ascending=False)

# Mostrar en texto (lo que ya tenías)
print("\n" + "="*30)
print(reporte)
print("="*30)

# --- NUEVO: Generar Gráfico ---
print("🎨 Dibujando gráfico...")

# Crear un gráfico de barras
plt.figure(figsize=(10, 6)) # Tamaño de la imagen
reporte.plot(kind='bar', color='teal')

plt.title('Mis Gastos por Categoría (2025)')
plt.ylabel('Monto en Soles (S/)')
plt.xlabel('Categoría')
plt.grid(axis='y', linestyle='--', alpha=0.7) # Rejilla suave

# Guardar la imagen en lugar de solo mostrarla
plt.savefig('mi_grafico_gastos.png')
print("✅ ¡Imagen 'mi_grafico_gastos.png' guardada con éxito!")
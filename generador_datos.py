import pandas as pd
import random
from datetime import datetime, timedelta

# Configuración
categorias = ['Comida', 'Transporte', 'Alquiler', 'Entretenimiento', 'Servicios']
num_filas = 50
datos = []

# Generar datos aleatorios
for _ in range(num_filas):
    fecha = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 300))
    categoria = random.choice(categorias)
    monto = round(random.uniform(20.0, 200.0), 2)
    datos.append([fecha.strftime("%Y-%m-%d"), categoria, monto])

# Crear DataFrame
df = pd.DataFrame(datos, columns=['Fecha', 'Categoria', 'Monto'])

# Guardar a CSV (Excel formato texto)
df.to_csv('mis_gastos.csv', index=False)

print("✅ Archivo 'mis_gastos.csv' generado con éxito con 50 filas.")
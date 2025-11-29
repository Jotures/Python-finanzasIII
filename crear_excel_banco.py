import pandas as pd
import random
from datetime import datetime, timedelta

# Configuración de simulación
num_filas = 100
categorias = ['Supermercado', 'Grifo', 'Restaurante', 'Transferencia', 'Suscripción', 'Farmacia']
bancos = ['BCP', 'Interbank', 'BBVA']

datos = []

print("🏦 Generando movimientos bancarios...")

for _ in range(num_filas):
    fecha = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 180))
    descripcion = f"COMPRA POS {random.choice(categorias).upper()} - {random.choice(bancos)}"
    # Generamos montos negativos (gastos) y positivos (ingresos)
    monto = round(random.uniform(-300.0, -10.0), 2) 
    
    # Un 10% de veces es un ingreso (sueldo)
    if random.random() > 0.9:
        descripcion = "ABONO HABERES"
        monto = round(random.uniform(2000.0, 3000.0), 2)
        
    datos.append([fecha, descripcion, monto])

# Crear DataFrame
df = pd.DataFrame(datos, columns=['Fecha Operación', 'Descripción', 'Importe'])

# GUARDAR COMO EXCEL REAL (.xlsx)
# index=False evita que se guarde la columna de números de fila 0,1,2...
df.to_excel('EstadoCuenta_2025.xlsx', index=False)

print("✅ ¡Listo! Archivo 'EstadoCuenta_2025.xlsx' creado.")
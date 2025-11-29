import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

print("🤖 Iniciando el robot...")

# 1. Configurar el acceso (La Llave)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# 2. Abrir la Hoja de Cálculo
# IMPORTANTE: Debe tener el nombre EXACTO que le pusiste en Google Sheets
nombre_hoja = "Finanzas Personales DB" 

try:
    print(f"📂 Buscando la hoja '{nombre_hoja}'...")
    sheet = client.open(nombre_hoja).sheet1  # Abre la primera pestaña
    
    # 3. Leer los datos y convertirlos a Pandas
    datos = sheet.get_all_records()
    df = pd.DataFrame(datos)
    
    print("\n✅ ¡CONEXIÓN EXITOSA! Aquí están tus datos de la nube:")
    print("-" * 40)
    print(df)
    print("-" * 40)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("Posibles causas:")
    print("1. El nombre del archivo en Google Sheets no es exacto.")
    print("2. No compartiste la hoja con el correo del robot.")

import pandas as pd
from pathlib import Path

# 1. CONFIGURACION DE RUTAS

BASE_DIR = Path(__file__).resolve().parent

# 2. ADQUISICION DE DATOS

transacciones = pd.read_csv(
    BASE_DIR / "datos" / "transacciones.csv"
)

productos = pd.read_excel(
    BASE_DIR / "datos" / "productos.xlsx",
    engine="openpyxl"
)

print("Archivos cargados correctamente.")

# 3. LIMPIEZA Y NORMALIZACION

# Convertir identificadores y valores numericos
transacciones["id_producto"] = pd.to_numeric(
    transacciones["id_producto"], errors="coerce"
)

productos["id_producto"] = pd.to_numeric(
    productos["id_producto"], errors="coerce"
)

transacciones["cantidad"] = pd.to_numeric(
    transacciones["cantidad"], errors="coerce"
)

productos["precio_unitario"] = pd.to_numeric(
    productos["precio_unitario"], errors="coerce"
)

# Convertir fechas
transacciones["fecha"] = pd.to_datetime(
    transacciones["fecha"],
    format="%d/%m/%Y",
    errors="coerce"
)

# Eliminar registros con datos criticos faltantes
transacciones = transacciones.dropna(
    subset=["id_producto", "cantidad", "fecha"]
)

productos = productos.dropna(
    subset=["id_producto", "nombre_producto", "precio_unitario"]
)

# Convertir identificadores a enteros
transacciones["id_producto"] = (
    transacciones["id_producto"].astype(int)
)

productos["id_producto"] = (
    productos["id_producto"].astype(int)
)

# Eliminar productos duplicados
productos = productos.drop_duplicates(
    subset=["id_producto"]
)

print("Limpieza y normalizacion completadas.")

# 4. INTEGRACION DE DATOS (MERGE)

ventas = pd.merge(
    transacciones,
    productos,
    on="id_producto",
    how="inner",
    validate="many_to_one"
)

print("Integracion de datos completada.")

# 5. CREACION DE LA COLUMNA CALCULADA

ventas["total_venta"] = (
    ventas["cantidad"] * ventas["precio_unitario"]
)

# 6. VERIFICACION DEL DATASET FINAL

print("\nDataset final:")
print(ventas.head())

print("\nDimensiones:", ventas.shape)

print("\nValores nulos:")
print(ventas.isnull().sum())

print("\nTotal general de ventas:")
print(ventas["total_venta"].sum())

# 7. EXPORTACION A PARQUET

ruta_salida = BASE_DIR / "ventas_final.parquet"

ventas.to_parquet(
    ruta_salida,
    index=False,
    engine="pyarrow"
)

# Comprobar el archivo generado
ventas_verificacion = pd.read_parquet(ruta_salida)

print("\nArchivo Parquet generado correctamente.")
print("Registros exportados:", len(ventas_verificacion))

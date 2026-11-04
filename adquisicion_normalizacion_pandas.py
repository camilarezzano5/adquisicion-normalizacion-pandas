
import pandas as pd
from pathlib import Path

# PASO 1: CONFIGURACION

BASE_DIR = Path(__file__).resolve().parent

# PASO 2: ADQUISICION DE DATOS

transacciones = pd.read_csv(
    BASE_DIR / "datos" / "transacciones.csv"
)

productos = pd.read_excel(
    BASE_DIR / "datos" / "productos.xlsx",
    engine="openpyxl"
)

print("Datos cargados correctamente.")

# PASO 3: LIMPIEZA Y NORMALIZACION

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

transacciones["fecha"] = pd.to_datetime(
    transacciones["fecha"],
    format="%d/%m/%Y",
    errors="coerce"
)

# Eliminar valores nulos en campos criticos

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

# Eliminar duplicados

productos = productos.drop_duplicates(
    subset=["id_producto"]
)

print("Limpieza completada.")

# PASO 4: INTEGRACION DE DATOS

ventas = pd.merge(
    transacciones,
    productos,
    on="id_producto",
    how="inner",
    validate="many_to_one"
)

print("Merge realizado correctamente.")

# PASO 5: COLUMNA CALCULADA

ventas["total_venta"] = (
    ventas["cantidad"] * ventas["precio_unitario"]
)

# PASO 6: VERIFICACION

print("\nPrimeras filas del dataset:")
print(ventas.head())

print("\nDimensiones:")
print(ventas.shape)

print("\nValores nulos:")
print(ventas.isnull().sum())

print("\nTipos de datos:")
print(ventas.dtypes)

print("\nTotal general de ventas:")
print(ventas["total_venta"].sum())

# PASO 7: EXPORTACION A PARQUET

ruta_salida = BASE_DIR / "ventas_final.parquet"

ventas.to_parquet(
    ruta_salida,
    index=False,
    engine="pyarrow"
)

# Comprobar exportacion

verificacion = pd.read_parquet(ruta_salida)

print("\nArchivo Parquet generado correctamente.")
print("Registros exportados:", len(verificacion))

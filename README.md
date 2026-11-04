
# Adquisición y Normalización con Pandas

## Descripción
Proyecto de integración de datos provenientes de dos fuentes:
CSV de transacciones y Excel de productos.

## Librerías
- Pandas
- Openpyxl
- PyArrow

## Ejecución
1. Instalar dependencias:
   pip install -r requirements.txt

2. Ejecutar:
   python adquisicion_normalizacion_pandas.py

## Proceso realizado
- Carga de CSV y Excel.
- Limpieza de datos.
- Conversión de fechas a datetime.
- Tratamiento de valores nulos.
- Integración mediante merge.
- Cálculo de total_venta.
- Exportación a Parquet.

## Resultado
Archivo final: ventas_final.parquet

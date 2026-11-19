# Análisis de los resultados de las pruebas Saber 11 en Boyacá mediante tecnologías Big Data

## Integrantes

- Samuel Avellaneda Guevara
- Fredy Mateo Niño Vásquez

Universidad Santo Tomás  
Ingeniería de Sistemas  
Asignatura: Big Data  
Periodo académico: 2026-2

## Descripción del proyecto

Este proyecto analiza los resultados de las pruebas Saber 11 en el departamento de Boyacá utilizando Python, Apache Spark, PySpark y Spark SQL.

Se procesaron inicialmente 215.234 registros y 51 variables, obtenidos del Portal de Datos Abiertos de Colombia. Después de las etapas de limpieza y transformación, se construyó un conjunto analítico de 100.049 registros y 19 variables.

El proyecto implementa una arquitectura Medallion con capas Bronce, Plata y Oro, y un dashboard interactivo mediante Streamlit y Plotly.

## Fuente de los datos

ICFES - Resultados únicos Saber 11.

https://www.datos.gov.co/d/kgxf-xxbe

Los registros se filtraron para el departamento de Boyacá utilizando el código departamental 15.

## Tecnologías utilizadas

- Python
- Pandas y NumPy
- Apache Spark y PySpark
- Spark SQL
- Streamlit
- Plotly
- Google Colab

## Arquitectura de datos

- Bronce: almacenamiento de los datos originales en CSV.
- Plata: datos limpiados y transformados mediante PySpark, almacenados en Parquet.
- Oro: tablas agregadas para el análisis académico, socioeconómico y territorial.
- Visualización: dashboard interactivo desarrollado en Streamlit.

## Estructura del proyecto

```text
Proyecto_BigData_Saber11_Boyaca/
    Proyecto_BigData_Saber11_Final.ipynb
    app.py
    requirements.txt
    README.md
    data/
        saber11_dashboard.csv.gz
```

## Instalación

Se requiere Python instalado en el computador.

Abrir una terminal en la carpeta del proyecto y ejecutar:

```bash
python -m pip install -r requirements.txt
```

## Ejecutar el dashboard

Antes de ejecutar la aplicación, comprobar que el archivo `saber11_dashboard.csv.gz` esté disponible en la ubicación esperada por `app.py`.

Ejecutar:

```bash
python -m streamlit run app.py
```

La aplicación se abrirá en el navegador.

## Procesamiento de datos

El archivo `Proyecto_BigData_Saber11_Final.ipynb` contiene el procesamiento realizado en Google Colab, incluyendo:

- Extracción de datos desde la API Socrata.
- Diagnóstico de calidad.
- Limpieza y transformación mediante PySpark.
- Construcción de las capas Medallion.
- Consultas mediante Spark SQL.
- Análisis estadístico y correlaciones.
- Generación de archivos para el dashboard.

## Resultados principales

El promedio global obtenido fue de 264,74 puntos.

Se identificaron diferencias en los resultados según la naturaleza de los colegios, el acceso a internet, el estrato socioeconómico, el nivel educativo de la madre y el municipio.

Estos resultados describen asociaciones estadísticas y no permiten establecer relaciones causales.

## Dashboard

El dashboard contiene seis visualizaciones y tres filtros interactivos.

Enlace público: pendiente de agregar o, alternativamente, ejecutar la aplicación siguiendo las instrucciones anteriores.

## Video de demostración

Enlace: pendiente de agregar.

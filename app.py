 
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# CONFIGURACIÓN
# ==========================================

st.set_page_config(
    page_title="Saber 11 - Boyacá",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Análisis de las Pruebas Saber 11 en Boyacá")
st.caption("Proyecto Integrador Big Data 2026-2 | Universidad Santo Tomás")

# ==========================================
# CARGA DE DATOS
# ==========================================

@st.cache_data
def cargar_datos():
    ruta = Path(__file__).resolve().parent / "data" / "saber11_dashboard.csv.gz"
    df = pd.read_csv(ruta, compression="gzip")

    for columna in [
        "punt_global", "anio", "cole_cod_mcpio_ubicacion"
    ]:
        df[columna] = pd.to_numeric(df[columna], errors="coerce")

    return df

try:
    df = cargar_datos()
except Exception as e:
    st.error(f"No se pudieron cargar los datos: {e}")
    st.stop()

# ==========================================
# FILTROS INTERACTIVOS
# ==========================================

st.sidebar.header("Filtros interactivos")

anios = sorted(df["anio"].dropna().unique().tolist())

filtro_anios = st.sidebar.multiselect(
    "Años",
    options=anios,
    default=anios
)

naturalezas = sorted(
    df["cole_naturaleza"].dropna().unique().tolist()
)

filtro_naturaleza = st.sidebar.multiselect(
    "Naturaleza del colegio",
    options=naturalezas,
    default=naturalezas
)

municipios = sorted(
    df["cole_mcpio_ubicacion"].dropna().unique().tolist()
)

filtro_municipios = st.sidebar.multiselect(
    "Municipios",
    options=municipios,
    default=municipios
)

# Aplicar los tres filtros
datos = df[
    df["anio"].isin(filtro_anios)
    & df["cole_naturaleza"].isin(filtro_naturaleza)
    & df["cole_mcpio_ubicacion"].isin(filtro_municipios)
].copy()

if datos.empty:
    st.warning("No hay registros para los filtros seleccionados.")
    st.stop()

# ==========================================
# INDICADORES GENERALES
# ==========================================

st.subheader("Indicadores generales")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Registros analizados", f"{len(datos):,}")
c2.metric("Puntaje global promedio", f"{datos['punt_global'].mean():.2f}")
c3.metric("Municipios", datos["cole_cod_mcpio_ubicacion"].nunique())
c4.metric(
    "Colegios oficiales (registros)",
    int(
        datos["cole_naturaleza"]
        .astype(str).str.upper()
        .eq("OFICIAL").sum()
    )
)

st.divider()

# ==========================================
# P1. EVOLUCIÓN TEMPORAL
# ==========================================

st.subheader("P1. Evolución temporal del puntaje global")

temporal = (
    datos.groupby("anio", as_index=False)
    .agg(
        promedio=("punt_global", "mean"),
        estudiantes=("punt_global", "size")
    )
)

# Evitar periodos con muestras muy pequeñas
temporal = temporal[temporal["estudiantes"] >= 1000]

fig1 = px.line(
    temporal,
    x="anio",
    y="promedio",
    markers=True,
    title="Puntaje global promedio por año",
    labels={"anio": "Año", "promedio": "Puntaje promedio"},
    hover_data=["estudiantes"]
)

st.plotly_chart(fig1, use_container_width=True)

# ==========================================
# P2. NATURALEZA DEL COLEGIO
# ==========================================

st.subheader("P2. Resultados según naturaleza del colegio")

naturaleza = (
    datos.groupby("cole_naturaleza", as_index=False)
    .agg(
        promedio=("punt_global", "mean"),
        estudiantes=("punt_global", "size")
    )
)

fig2 = px.bar(
    naturaleza,
    x="cole_naturaleza",
    y="promedio",
    color="cole_naturaleza",
    title="Promedio global: oficial y no oficial",
    labels={
        "cole_naturaleza": "Naturaleza",
        "promedio": "Puntaje promedio"
    },
    hover_data=["estudiantes"]
)

st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# P3. ACCESO A INTERNET
# ==========================================

st.subheader("P3. Factores socioeconómicos")

internet = (
    datos.groupby("fami_tieneinternet", as_index=False)
    .agg(
        promedio=("punt_global", "mean"),
        estudiantes=("punt_global", "size")
    )
)

fig3 = px.bar(
    internet,
    x="fami_tieneinternet",
    y="promedio",
    color="fami_tieneinternet",
    title="Puntaje global según acceso a internet",
    labels={
        "fami_tieneinternet": "Acceso a internet",
        "promedio": "Puntaje promedio"
    },
    hover_data=["estudiantes"]
)

st.plotly_chart(fig3, use_container_width=True)

# ==========================================
# P3. ESTRATO SOCIOECONÓMICO
# ==========================================

estrato = (
    datos.groupby("fami_estratovivienda", as_index=False)
    .agg(
        promedio=("punt_global", "mean"),
        estudiantes=("punt_global", "size")
    )
)

fig4 = px.bar(
    estrato,
    x="fami_estratovivienda",
    y="promedio",
    title="Puntaje global según estrato socioeconómico",
    labels={
        "fami_estratovivienda": "Estrato",
        "promedio": "Puntaje promedio"
    },
    hover_data=["estudiantes"]
)

st.plotly_chart(fig4, use_container_width=True)

# ==========================================
# P3. EDUCACIÓN DE LA MADRE
# ==========================================

educacion = (
    datos.groupby("fami_educacionmadre", as_index=False)
    .agg(
        promedio=("punt_global", "mean"),
        estudiantes=("punt_global", "size")
    )
    .sort_values("promedio")
)

fig5 = px.bar(
    educacion,
    x="promedio",
    y="fami_educacionmadre",
    orientation="h",
    title="Puntaje según nivel educativo de la madre",
    labels={
        "promedio": "Puntaje promedio",
        "fami_educacionmadre": "Nivel educativo"
    },
    hover_data=["estudiantes"],
    height=550
)

st.plotly_chart(fig5, use_container_width=True)

# ==========================================
# P4. ANÁLISIS POR MUNICIPIO
# ==========================================

st.subheader("P4. Comparación territorial")

por_municipio = (
    datos.groupby(
        ["cole_cod_mcpio_ubicacion", "cole_mcpio_ubicacion"],
        as_index=False
    )
    .agg(
        promedio=("punt_global", "mean"),
        estudiantes=("punt_global", "size")
    )
)

por_municipio = por_municipio[
    por_municipio["estudiantes"] >= 100
]

por_municipio = (
    por_municipio.nlargest(15, "promedio")
    .sort_values("promedio")
)

fig6 = px.bar(
    por_municipio,
    x="promedio",
    y="cole_mcpio_ubicacion",
    orientation="h",
    title="15 municipios con mayor promedio (mínimo 100 registros)",
    labels={
        "promedio": "Puntaje promedio",
        "cole_mcpio_ubicacion": "Municipio"
    },
    hover_data=["estudiantes"],
    height=600
)

st.plotly_chart(fig6, use_container_width=True)

# ==========================================
# INFORMACIÓN FINAL
# ==========================================

st.divider()

st.info(
    "Los resultados corresponden a asociaciones estadísticas "
    "descriptivas y no permiten establecer relaciones causales."
)

st.caption(
    "Fuente: ICFES - Resultados únicos Saber 11. "
    "Procesamiento mediante PySpark y Spark SQL."
)

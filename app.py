import streamlit as st
import json
import os
from datetime import date
import pandas as pd


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="RedZone Fitness",
    page_icon="🔥",
    layout="wide"
)

ARCHIVO_DATOS = "datos_peso.json"


# =========================================================
# DATOS
# =========================================================

def datos_iniciales():
    return {
        "perfil": {
            "nombre": "",
            "edad": 30,
            "altura": 170.0
        },
        "objetivo": {
            "peso": 70.0,
            "fecha": str(date.today())
        },
        "pesos": []
    }


def cargar_datos():

    if not os.path.exists(ARCHIVO_DATOS):
        return datos_iniciales()

    try:

        with open(
            ARCHIVO_DATOS,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(archivo)

        base = datos_iniciales()

        if "perfil" not in datos:
            datos["perfil"] = base["perfil"]

        if "objetivo" not in datos:
            datos["objetivo"] = base["objetivo"]

        if "pesos" not in datos:
            datos["pesos"] = []

        return datos

    except Exception:

        return datos_iniciales()


def guardar_datos(datos):

    temporal = ARCHIVO_DATOS + ".tmp"

    with open(
        temporal,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    os.replace(
        temporal,
        ARCHIVO_DATOS
    )


datos = cargar_datos()


# =========================================================
# ESTILO
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(255, 0, 55, 0.20),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 90%,
                rgba(190, 0, 30, 0.18),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #020202 0%,
                #160005 50%,
                #030303 100%
            );
    }

    [data-testid="stSidebar"] {
        background-color: #080808;
        border-right: 1px solid #35000b;
    }

    h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
    }

    h2, h3 {
        color: #ffffff !important;
    }

    p, label {
        color: #dddddd;
    }

    .stButton > button {
        background-color: #e50935;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: bold;
        padding: 0.6rem 1rem;
    }

    .stButton > button:hover {
        background-color: #ff1744;
        color: white;
    }

    [data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #151515,
                #090909
            );

        border: 1px solid #3a0710;
        border-radius: 16px;
        padding: 18px;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
    }

    [data-testid="stMetricLabel"] {
        color: #bbbbbb;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CABECERA
# =========================================================

nombre = datos["perfil"].get(
    "nombre",
    ""
)

st.title("🔥 REDZONE FITNESS")

if nombre:
    st.write(
        f"Bienvenido de nuevo, **{nombre}**."
    )
else:
    st.write(
        "Tu progreso. Tu objetivo. Tu camino."
    )


# =========================================================
# MENÚ
# =========================================================

pagina = st.sidebar.radio(
    "MENÚ",
    [
        "🏠 Inicio",
        "👤 Mi perfil",
        "🎯 Mi objetivo",
        "⚖️ Registrar peso",
        "📊 Historial"
    ]
)


# =========================================================
# PERFIL
# =========================================================

if pagina == "👤 Mi perfil":

    st.header("👤 Mi perfil")

    perfil = datos["perfil"]

    nombre = st.text_input(
        "Nombre",
        value=perfil.get(
            "nombre",
            ""
        )
    )

    edad = st.number_input(
        "Edad",
        min_value=1,
        max_value=120,
        value=int(
            perfil.get(
                "edad",
                30
            )
        ),
        step=1
    )

    altura = st.number_input(
        "Altura (cm)",
        min_value=50.0,
        max_value=250.0,
        value=float(
            perfil.get(
                "altura",
                170.0
            )
        ),
        step=0.5
    )

    st.write("")

    if st.button(
        "💾 Guardar perfil"
    ):

        datos["perfil"] = {
            "nombre": nombre,
            "edad": edad,
            "altura": altura
        }

        guardar_datos(datos)

        st.success(
            "Perfil guardado correctamente."
        )

        st.rerun()


# =========================================================
# OBJETIVO
# =========================================================

elif pagina == "🎯 Mi objetivo":

    st.header("🎯 Mi objetivo")

    objetivo = datos["objetivo"]

    peso_objetivo_actual = float(
        objetivo.get(
            "peso",
            70.0
        )
    )

    try:

        fecha_objetivo_actual = date.fromisoformat(
            objetivo.get(
                "fecha",
                str(date.today())
            )
        )

    except Exception:

        fecha_objetivo_actual = date.today()

    peso_objetivo = st.number_input(
        "🎯 Peso objetivo (kg)",
        min_value=1.0,
        max_value=500.0,
        value=peso_objetivo_actual,
        step=0.1
    )

    fecha_objetivo = st.date_input(
        "📅 Fecha objetivo",
        value=fecha_objetivo_actual
    )

    st.write("")

    if st.button(
        "🎯 Guardar objetivo"
    ):

        datos["objetivo"] = {
            "peso": peso_objetivo,
            "fecha": str(
                fecha_objetivo
            )
        }

        guardar_datos(datos)

        st.success(
            "Objetivo guardado correctamente."
        )

        st.rerun()


# =========================================================
# REGISTRAR PESO
# =========================================================

elif pagina == "⚖️ Registrar peso":

    st.header("⚖️ Registrar peso")

    st.write(
        "Registra tu peso para construir tu historial."
    )

    fecha_peso = st.date_input(
        "📅 Fecha",
        value=date.today()
    )

    peso = st.number_input(
        "⚖️ Peso (kg)",
        min_value=1.0,
        max_value=500.0,
        value=70.0,
        step=0.1
    )

    st.write("")

    if st.button(
        "🔥 Guardar peso",
        type="primary"
    ):

        nuevo = {
            "fecha": str(fecha_peso),
            "peso": float(peso)
        }

        datos["pesos"].append(
            nuevo
        )

        datos["pesos"].sort(
            key=lambda x: x["fecha"]
        )

        guardar_datos(datos)

        st.success(
            f"Registro guardado: {peso:.1f} kg"
        )

        st.rerun()


# =========================================================
# INICIO
# =========================================================

elif pagina == "🏠 Inicio":

    st.header("📊 Mi progreso")

    pesos = datos["pesos"]

    if not pesos:

        st.info(
            "Todavía no tienes registros de peso."
        )

        st.write(
            "Ve a **⚖️ Registrar peso** para comenzar."
        )

    else:

        df = pd.DataFrame(pesos)

        df["fecha"] = pd.to_datetime(
            df["fecha"]
        )

        df["peso"] = pd.to_numeric(
            df["peso"]
        )

        df = df.sort_values(
            "fecha"
        )

        peso_actual = float(
            df.iloc[-1]["peso"]
        )

        peso_inicial = float(
            df.iloc[0]["peso"]
        )

        peso_objetivo = float(
            datos["objetivo"].get(
                "peso",
                70.0
            )
        )

        # -----------------------------------------
        # MÉTRICAS
        # -----------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "⚖️ Peso actual",
                f"{peso_actual:.1f} kg"
            )

        with col2:

            st.metric(
                "🏁 Peso inicial",
                f"{peso_inicial:.1f} kg"
            )

        with col3:

            st.metric(
                "🎯 Objetivo",
                f"{peso_objetivo:.1f} kg"
            )

        st.write("")

        # -----------------------------------------
        # CAMBIO TOTAL
        # -----------------------------------------

        cambio = (
            peso_actual -
            peso_inicial
        )

        st.metric(
            "📉 Cambio desde el inicio",
            f"{cambio:+.1f} kg"
        )

        # -----------------------------------------
        # GRÁFICA
        # -----------------------------------------

        st.subheader(
            "📈 Evolución del peso"
        )

        grafica = df.set_index(
            "fecha"
        )[["peso"]]

        st.line_chart(
            grafica,
            width="stretch"
        )

        # -----------------------------------------
        # OBJETIVO
        # -----------------------------------------

        st.subheader(
            "🎯 Progreso hacia tu objetivo"
        )

        diferencia = (
            peso_actual -
            peso_objetivo
        )

        if abs(diferencia) < 0.05:

            st.success(
                "🎉 Has llegado al peso objetivo registrado."
            )

            st.progress(100)

        elif peso_inicial != peso_objetivo:

            progreso = (
                (peso_inicial - peso_actual)
                /
                (peso_inicial - peso_objetivo)
            ) * 100

            progreso = max(
                0,
                min(100, progreso)
            )

            st.progress(
                int(progreso)
            )

            st.write(
                f"Progreso estimado: **{progreso:.1f}%**"
            )

            st.write(
                f"Distancia actual al objetivo: "
                f"**{abs(diferencia):.1f} kg**"
            )

        else:

            st.info(
                "Registra un objetivo diferente "
                "al peso inicial para calcular el progreso."
            )

        # -----------------------------------------
        # FECHA OBJETIVO
        # -----------------------------------------

        fecha_objetivo = datos["objetivo"].get(
            "fecha"
        )

        if fecha_objetivo:

            try:

                fecha = date.fromisoformat(
                    fecha_objetivo
                )

                st.info(
                    f"📅 Fecha objetivo: "
                    f"**{fecha.strftime('%d/%m/%Y')}**"
                )

            except Exception:

                pass

        # -----------------------------------------
        # AVISO MÉDICO
        # -----------------------------------------

        st.warning(
            """
            ⚠️ **Aviso de seguridad**

            Esta aplicación es únicamente una herramienta
            para registrar y visualizar cambios de peso.
            No realiza diagnósticos ni sustituye la valoración
            de un profesional sanitario.

            Evita objetivos extremos o cambios de peso
            demasiado rápidos. Las necesidades de cada persona
            pueden ser diferentes.

            Si tienes una enfermedad, estás embarazada, eres
            menor de edad, tienes antecedentes de un trastorno
            alimentario o quieres realizar un cambio importante
            de peso, consulta con un profesional sanitario.
            """
        )


# =========================================================
# HISTORIAL
# =========================================================

elif pagina == "📊 Historial":

    st.header("📊 Historial")

    pesos = datos["pesos"]

    if not pesos:

        st.info(
            "No tienes registros todavía."
        )

    else:

        df = pd.DataFrame(pesos)

        df["fecha"] = pd.to_datetime(
            df["fecha"]
        )

        df["peso"] = pd.to_numeric(
            df["peso"]
        )

        df = df.sort_values(
            "fecha"
        )

        # -----------------------------------------
        # GRÁFICA
        # -----------------------------------------

        st.subheader(
            "📈 Gráfica"
        )

        st.line_chart(
            df.set_index("fecha")["peso"],
            width="stretch"
        )

        # -----------------------------------------
        # TABLA
        # -----------------------------------------

        st.subheader(
            "📋 Registros guardados"
        )

        tabla = df.copy()

        tabla["fecha"] = tabla[
            "fecha"
        ].dt.strftime(
            "%d/%m/%Y"
        )

        tabla["peso"] = tabla[
            "peso"
        ].round(1)

        tabla = tabla.rename(
            columns={
                "fecha": "Fecha",
                "peso": "Peso (kg)"
            }
        )

        st.dataframe(
            tabla,
            width="stretch",
            hide_index=True
        )

        # -----------------------------------------
        # ELIMINAR
        # -----------------------------------------

        st.subheader(
            "🗑️ Eliminar registro"
        )

        opciones = []

        for registro in pesos:

            opciones.append(
                f"{registro['fecha']} — "
                f"{float(registro['peso']):.1f} kg"
            )

        seleccionado = st.selectbox(
            "Selecciona el registro que quieres eliminar",
            opciones
        )

        if st.button(
            "🗑️ Eliminar registro"
        ):

            indice = opciones.index(
                seleccionado
            )

            datos["pesos"].pop(
                indice
            )

            guardar_datos(datos)

            st.success(
                "Registro eliminado."
            )

            st.rerun()

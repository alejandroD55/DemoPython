import streamlit as st
from services.ai_client import *
from services.functions import (
    leer_txt,
    rutina_json_a_excel_bytes,
    rutina_json_a_dataframe,
    dieta_json_a_dataframe,
    rutina_de_entreno,
    generacion_de_plan_de_nutricion,
    dietas_json_a_excel_bytes,
)
from services.logger import logger


# Título de la app
st.title("Dietista GPT")
st.subheader("Asistente de salud y bienestar")
st.write(
    "Por favor, proporciona información sobre tu edad, peso, altura, sexo y nivel de actividad para obtener recomendaciones personalizadas."
)
# Caja de texto para el mensaje del usuario
edad = st.text_input("Edad", placeholder="Escribe tu edad")
peso = st.text_input("Peso", placeholder="Escribe tu peso")
altura = st.text_input("Altura", placeholder="Escribe tu altura")
sexo = st.selectbox("Sexo", ["Hombre", "Mujer"])
nivel_actividad = st.selectbox("Nivel de actividad", ["Bajo", "Moderado", "Alto"])
user_message = (
    "Edad:"
    + edad
    + " "
    + "Peso:"
    + peso
    + " "
    + "Altura:"
    + altura
    + " "
    + "Sexo:"
    + sexo
    + " "
    + "Nivel de actividad:"
    + nivel_actividad
)


# Botón para enviar
if st.button("Enviar"):
    if user_message.strip() == "":
        st.warning("Por favor, escribe un mensaje antes de enviar.")
    else:
        with st.spinner("🏋️‍♂️ Consultando a tu entrenador..."):

            rutina = rutina_de_entreno(user_message)
        with st.spinner("🍲 Consultando a tu dietista..."):

            dieta = generacion_de_plan_de_nutricion(user_message)

        st.success("Respuesta recibida:")

        # Convertir JSON a DataFrame
        tabla_df_entrenador = rutina_json_a_dataframe(rutina)
        tabla_df_dieta = dieta_json_a_dataframe(dieta)

        # Mostrar la tabla
        st.markdown("### 🏋️‍♂️ Tabla de ejercicios")
        st.dataframe(tabla_df_entrenador, use_container_width=True)
        # Mostrar la tabla
        st.markdown("### 🍲 Dieta")
        st.dataframe(tabla_df_dieta, use_container_width=True)

        # Botón de descarga Excel
        excel_bytes_rutina = rutina_json_a_excel_bytes(rutina)
        excel_bytes_dieta = dietas_json_a_excel_bytes(dieta)
        st.download_button(
            label="📥 Descargar rutina en Excel",
            data=excel_bytes_rutina,
            file_name="rutina_entrenamiento.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        st.download_button(
            label="📥 Descargar dieta en Excel",
            data=excel_bytes_dieta,
            file_name="dieta.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

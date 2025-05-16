import json
from openpyxl import Workbook
from io import BytesIO
import pandas as pd
from config import *
from services.logger import logger
from .ai_client import *


def leer_txt(ruta_archivo: str) -> str:
    """
    Lee un archivo .txt y devuelve su contenido como string.
    """
    ruta_archivo = PROMPTS_FOLDER + ruta_archivo
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        return contenido
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_archivo}")
        return ""
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return ""


def rutina_json_a_excel_bytes(data) -> BytesIO:
    data = json.loads(data)
    wb = Workbook()
    ws = wb.active
    ws.title = "Rutina de entrenamiento"

    ws.append(["Día", "Ejercicio", "Series", "Repeticiones", "Explicación"])
    for dia, contenido in data.items():
        for ejercicio in contenido["Ejercicios"]:
            for nombre, detalle in ejercicio.items():
                ws.append(
                    [
                        dia,
                        nombre,
                        detalle["Series"],
                        detalle["Repeticiones"],
                        detalle["Explicacion del ejercicio"],
                    ]
                )

    # Guardar en memoria
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output


def dietas_json_a_excel_bytes(data) -> BytesIO:
    """
    Convierte un JSON de dietas a un archivo Excel en memoria y lo devuelve como BytesIO.
    Soporta listas de ingredientes y convierte todo a texto plano.
    """
    if isinstance(data, str):
        data = json.loads(data)

    wb = Workbook()
    ws = wb.active
    ws.title = "Plan de Dieta"

    # Cabecera
    ws.append(
        [
            "Día",
            "Comida",
            "Plato",
            "Ingredientes",
            "Calorías",
            "Aporte nutricional",
            "Preparación",
        ]
    )

    for dia, contenido in data.items():
        comidas = contenido.get("Comidas", {})
        for nombre_comida, detalle in comidas.items():
            ingredientes = detalle.get("Ingredientes", "")
            if isinstance(ingredientes, list):
                ingredientes = ", ".join(ingredientes)

            aporte = detalle.get("Aporte nutricional", "")
            if isinstance(aporte, list):
                aporte = ", ".join(aporte)

            ws.append(
                [
                    dia,
                    nombre_comida,
                    detalle.get("Plato", ""),
                    ingredientes,
                    detalle.get("Calorias", ""),
                    aporte,
                    detalle.get("Preparacion", ""),
                ]
            )

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output


def rutina_json_a_dataframe(data) -> pd.DataFrame:
    """
    Convierte la rutina JSON en un DataFrame para visualizar en Streamlit.
    """
    data = json.loads(data)
    filas = []
    for dia, contenido in data.items():
        for ejercicio in contenido.get("Ejercicios", []):
            for nombre, detalle in ejercicio.items():
                filas.append(
                    {
                        "Día": dia,
                        "Ejercicio": nombre,
                        "Series": detalle.get("Series"),
                        "Repeticiones": detalle.get("Repeticiones"),
                        "Explicación": detalle.get("Explicacion del ejercicio"),
                    }
                )
    return pd.DataFrame(filas)


def dieta_json_a_dataframe(data: dict) -> pd.DataFrame:
    """
    Convierte un JSON con estructura de comidas por día (7 días) a un DataFrame plano.
    """
    if isinstance(data, str):
        data = json.loads(data)

    filas = []
    for dia, contenido in data.items():
        comidas = contenido.get("Comidas", {})
        for tipo_comida, detalles in comidas.items():
            filas.append(
                {
                    "Día": dia,
                    "Comida": tipo_comida,
                    "Plato": detalles.get("Plato", ""),
                    "Ingredientes": detalles.get("Ingredientes", ""),
                    "Calorías": detalles.get("Calorias", ""),
                    "Aporte nutricional": detalles.get("Aporte nutricional", ""),
                    "Preparación": detalles.get("Preparacion", ""),
                }
            )

    return pd.DataFrame(filas)


def rutina_de_entreno(user_message: str):
    system_message_entrenador = leer_txt("system_message_entrenador.txt")
    prompt_entrenador = compose_prompt(
        user_message=user_message, system_message=system_message_entrenador
    )

    logger.info(f"Prompt enviado: {prompt_entrenador}")
    respuesta_entrenador = extract_entities(prompt_entrenador, "gpt-4o-mini")
    return respuesta_entrenador


def generacion_de_plan_de_nutricion(user_message: str):
    system_message_nutricion = leer_txt("system_message_nutricion.txt")
    prompt_nutricion = compose_prompt(
        user_message=user_message, system_message=system_message_nutricion
    )

    logger.info(f"Prompt enviado: {prompt_nutricion}")
    respuesta_nutricion = extract_entities(prompt_nutricion, "gpt-4o-mini")
    return respuesta_nutricion

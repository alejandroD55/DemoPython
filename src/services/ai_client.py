from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI()


def compose_prompt(user_message: str, system_message: str) -> str:
    """
    Recibe un diccionario con información y devuelve un prompt natural para GPT.
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    return messages


def extract_entities(messages: list, model: str = "gpt-4") -> dict:
    """
    Envía mensajes a la API y devuelve la respuesta del modelo como JSON si es posible.
    """
    try:
        response = client.chat.completions.create(
            model=model, messages=messages, temperature=0.6
        )
        content = response.choices[0].message.content

        return content

    except Exception as e:
        print("❌ Error al extraer entidades:", e)
        return {}

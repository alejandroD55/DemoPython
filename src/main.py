from services.ai_client import *

if __name__ == "__main__":
    prompt = compose_prompt(
        user_message="¿Cuáles son los síntomas de la gripe?",
        system_message="Eres un asistente médico que responde preguntas sobre salud."
    )
    respuesta = extract_entities(prompt,"gpt-4o-mini")
    print(respuesta)    
    
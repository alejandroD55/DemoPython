from pydantic import BaseModel
from typing import List, Optional


class Comida(BaseModel):
    tipo: str  # desayuno, comida, cena, snack
    alimentos: List[str]
    calorias: Optional[int] = None
    notas: Optional[str] = None


class Dieta(BaseModel):
    objetivo: str  # perder grasa, mantener, ganar músculo, etc.
    calorias_totales: Optional[int] = None
    comidas: List[Comida]


class Ejercicio(BaseModel):
    nombre: str
    series: int
    repeticiones: Optional[int] = None
    duracion_minutos: Optional[float] = None
    musculo_principal: Optional[str] = None


class Entrenamiento(BaseModel):
    dia: str  # Ej: "lunes"
    ejercicios: List[Ejercicio]


class Rutina(BaseModel):
    objetivo: str  # fuerza, hipertrofia, mantenimiento, rehabilitación
    frecuencia_semanal: int
    entrenamientos: List[Entrenamiento]

from dataclasses import dataclass
from typing import Optional

@dataclass
class ResultadoOperacion:
    exito: bool
    mensaje: str

@dataclass
class ResultadoCompletar(ResultadoOperacion):
    puntaje: int = 0
    mensaje_racha: Optional[str] = None
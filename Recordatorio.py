import requests
from storage import cargar_datos
from config import *
import os
from datetime import datetime
os.chdir("/home/emersondavid/Documentos/P/Phyton/Programa_De_Practica/Proyectos/Gestor_Tareas")
def revisar_y_enviar():
    tareas, historial, puntos, tareas_rutina,registro_cumplidos, webhook = cargar_datos()

    hora_actual = datetime.now().strftime("%H:%M")
    pendientes = []
    for prioridad in ["Alta","Media","Baja"]:
        for t in tareas_rutina:
            if t.prioridad == prioridad and t.hora is not None and t.hora == hora_actual:
                pendientes.append(f"- {t.nombre} ({t.prioridad})({t.hora})")

    if pendientes:
        mensaje_texto = "Tareas pendientes:\n" + "\n".join(pendientes)
    else:
        return

    requests.post(webhook, json={"content": mensaje_texto})


if __name__ == "__main__":
    revisar_y_enviar()
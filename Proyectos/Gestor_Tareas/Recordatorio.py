import requests
from storage import cargar_datos
import os
from datetime import datetime
os.chdir("/home/emerson/Escritorio/Automatizar/Gestor_tareas")

WEBHOOK_URL = "PON_TU_WEBHOOK_AQUI"

def revisar_y_enviar():
    tareas, historial, puntos = cargar_datos()
    hora_actual = datetime.now().strftime("%H:%M")
    pendientes = []
    for prioridad in ["Alta","Media","Baja"]:
        for t in tareas:
            if t["Prioridad"] == prioridad and t["Estado"] == "Pendiente" and t["Hora"] is not None and t["Hora"] == hora_actual:
                pendientes.append(f"- {t['Nombre']} ({t['Prioridad']})({t['Hora']})")

    if pendientes:
        mensaje_texto = "Tareas pendientes:\n" + "\n".join(pendientes)
    else:
        return

    requests.post(WEBHOOK_URL, json={"content": mensaje_texto})


if __name__ == "__main__":
    revisar_y_enviar()
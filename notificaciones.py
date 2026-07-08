from plyer import notification
import subprocess
import os
from datetime import datetime
from babel.dates import get_day_names
import random
import time
from src.base_sql import cargar_tareas
from src.storage import cargar_datos
from config_logs import crear_log

RUTA_MEMORIA_NOTI = "/tmp/ultima_noti_disciplina.txt"

import sys
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RUTA_ASSETS = os.path.join(BASE_DIR, "assets")

RUTA_SONIDO = os.path.join(RUTA_ASSETS, "dota2-notification.mp3")
RUTA_ICONO = os.path.join(RUTA_ASSETS, "icono.png")

def notificacion_tareas(titulo, mensaje):
    print("Reproduciendo sonido:", RUTA_SONIDO)
    subprocess.Popen(["paplay", RUTA_SONIDO])
    notification.notify(
        title=f"🥊 {titulo}",
        message=mensaje,
        app_name='Gestor de Disciplina',
        app_icon=RUTA_ICONO,
        timeout=10
    )

def enviar_notificacion():

    ultima_notificacion = ""
    if os.path.exists(RUTA_MEMORIA_NOTI):
        with open(RUTA_MEMORIA_NOTI, "r") as f:
            ultima_notificacion = f.read().strip()
    
    hora = datetime.now().strftime("%H:%M")
    fecha = datetime.now().strftime("%d/%m/%Y")

    hoy = datetime.now()

    nombres_dias = get_day_names('wide', locale='es')
    dia_hoy = nombres_dias[hoy.weekday()]

    puntos, webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    tareas,tareas_rutina = cargar_tareas()

    frase_motivadora = random.choice(lista_frases) if lista_frases else "Que tu disciplina no flaquee."

    for tarea in tareas + tareas_rutina:
        if tarea.hora is None:
            pass
        else:
            if tarea.hora == hora:
                id_tarea = f"{tarea.nombre}:{tarea.hora}:{fecha}"

                if tarea.tipo == "Unica":
                    if ultima_notificacion != id_tarea and tarea.estado == "Pendiente":
                        notificacion_tareas(tarea.nombre.title(),f"Ya es hora de completar la tarea de {tarea.nombre} \n{frase_motivadora}")
                        crear_log("INFO",f"Se envio una notifcación de la tarea {tarea}")

                        with open(RUTA_MEMORIA_NOTI, "w") as f:
                            f.write(id_tarea)
                        return
                else:
                    if f"Habito completado el {fecha}" in tarea.estado:
                        return
                    elif tarea.estado == "Pendiente" and ultima_notificacion != id_tarea and dia_hoy in tarea.dias:
                        print(f"Enviado {tarea.estado} Pendiente")
                        notificacion_tareas(tarea.nombre.title(),f"Ya es hora de completar la tarea de {tarea.nombre} \n{frase_motivadora}")
                        crear_log("INFO",f"Se envio una notifcación de la tarea {tarea}")
                        with open(RUTA_MEMORIA_NOTI, "w") as f:
                            f.write(id_tarea)

                    elif ultima_notificacion != id_tarea and dia_hoy in tarea.dias:
                        print(f"Enviando {tarea.estado}")
                        notificacion_tareas(tarea.nombre.title(),f"Ya es hora de completar la tarea de {tarea.nombre} \n{frase_motivadora}")
                        crear_log("INFO",f"Se envio una notifcación de la tarea {tarea}")
                        with open(RUTA_MEMORIA_NOTI, "w") as f:
                            f.write(id_tarea)

                        print(f"✅ Notificado: {id_tarea}")
                        return
                    else:
                        print("No notifique rutina")

def enviar_notificacion_diaria():

    hora = datetime.now().strftime("%H:%M")
    fecha = datetime.now().strftime("%d/%m/%Y")

    tareas, tareas_rutina = cargar_tareas()

    todos = tareas + tareas_rutina
    faltantes = False

    for tarea in todos:
        if tarea.estado == "Pendiente" or tarea.estado != f"Habito completado el {fecha}":
            faltantes = True
    
    if todos:
        if faltantes:
            if hora == "20:00":
                print(f"Enviando Notificación diaria {hora}")
                notificacion_tareas("Evaluacion Diaria", "¿Ya registraste tus habitos y tareas? ¡Aun estas a tiempo!")
        else:
            if hora == "20:00":
                notificacion_tareas("Evaluacion Diaria", "Felicidades hoy hiciste un buen trabajo")

def daemon_notificaciones():
    print("🚀 Vigilante de Disciplina iniciado...")
    print("Version 1.5")

    while True:
        enviar_notificacion_diaria()
        enviar_notificacion()
        time.sleep(60)

if __name__ == "__main__":
    daemon_notificaciones()
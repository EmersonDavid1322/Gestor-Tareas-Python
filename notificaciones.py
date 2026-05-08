from plyer import notification
from playsound import playsound
import subprocess
import os
from datetime import datetime
from babel.dates import get_day_names
import random
import time
from storage import cargar_datos

RUTA_MEMORIA_NOTI = "/tmp/ultima_noti_disciplina.txt"

import sys
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RUTA_SONIDO = os.path.join(BASE_DIR, "noti", "dota2-notification.mp3")

def notificacion_tareas(titulo, mensaje):
    print("Reproduciendo sonido:", RUTA_SONIDO)
    subprocess.Popen(["paplay", RUTA_SONIDO])
    notification.notify(
        title=f"🥊 {titulo}",
        message=mensaje,
        app_name='Gestor de Disciplina',
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

    tareas, historial, puntos_v, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

    frase_motivadora = random.choice(lista_frases) if lista_frases else "Que tu disciplina no flaquee."

    for tarea in tareas + tareas_rutina:
        if tarea.hora is None:
            pass
        else:
            if tarea.hora == hora:
                id_tarea = f"{tarea.nombre}:{tarea.hora}:{fecha}"

                if tarea.tipo == "Unica":
                    print("ENTRÓ AL IF 🔥 Unica")
                    if ultima_notificacion != id_tarea and tarea.estado == "Pendiente":
                        notificacion_tareas(tarea.nombre.title(),f"Ya es hora de completar la tarea de {tarea.nombre} \n{frase_motivadora}")
                    
                        with open(RUTA_MEMORIA_NOTI, "w") as f:
                            f.write(id_tarea)

                        print(f"✅ Notificado: {id_tarea}")
                        return
                else:
                    print("Rutina")
                    if str(fecha) in tarea.estado:
                        print("Fecha conside con estado")
                        return
                    elif tarea.estado == "Pendiente" and ultima_notificacion != id_tarea and dia_hoy in tarea.dias:
                        print(f"Enviado {tarea.estado} Pendiente")
                        notificacion_tareas(tarea.nombre.title(),f"Ya es hora de completar la tarea de {tarea.nombre} \n{frase_motivadora}")

                        with open(RUTA_MEMORIA_NOTI, "w") as f:
                            f.write(id_tarea)

                    elif ultima_notificacion != id_tarea and dia_hoy in tarea.dias:
                        print(f"Enviando {tarea.estado}")
                        notificacion_tareas(tarea.nombre.title(),f"Ya es hora de completar la tarea de {tarea.nombre} \n{frase_motivadora}")
                    
                        with open(RUTA_MEMORIA_NOTI, "w") as f:
                            f.write(id_tarea)

                        print(f"✅ Notificado: {id_tarea}")
                        return
                    else:
                        print("No notifique")

def enviar_notificacion_diaria():
    hora = datetime.now().strftime("%H:%M")
    fecha = datetime.now().strftime("%d/%m/%Y")

    tareas, historial, puntos_v, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

    todos = tareas + tareas_rutina
    faltantes = False

    for tarea in todos:
        if tarea.estado == "Pendiente" or tarea.estado != f"Habito completado el {fecha}":
            faltantes = True
    
    if todos:
        if faltantes:
            if hora == "21:00":
                print("aqui")
                print(f"Enviando Notificación diaria {hora}")
                notificacion_tareas("Evaluacion Diaria", "¿Ya registraste tus habitos y tareas? ¡Aun estas a tiempo!")
        else:
            if hora == "21:00":
                notificacion_tareas("Evaluacion Diaria", "Felicidades hoy hiciste un buen trabajo")

def daemon_notificaciones():
    print("🚀 Vigilante de Disciplina iniciado...")
    print("Version 1.2")

    while True:
        enviar_notificacion_diaria()
        enviar_notificacion()
        time.sleep(15)

if __name__ == "__main__":
    daemon_notificaciones()
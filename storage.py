import json
import os 
from clases import Tarea, TareaRutina
os.makedirs("data", exist_ok=True)


def guardar_datos(tareas,historial,puntos,tareas_rutina,registro_cumplidos,webhook): 

    tareas_json = []
    for tarea in tareas:
        tareas_json.append(tarea.a_diccionario())

    tareas_rutina_json = []
    for rutina in tareas_rutina:
        tareas_rutina_json.append(rutina.a_diccionario())

    with open("data/datos_gestor.json", "w") as f:
        json.dump({
            "tareas": tareas_json,
            "rutinas": tareas_rutina_json,
            "registro": registro_cumplidos
        }, f, indent=4, ensure_ascii=False)

    with open("data/historial.json", "w") as f: 
        json.dump(historial,f, indent=4, ensure_ascii=False)
    
    with open("data/puntaje.json","w") as f:
        json.dump(puntos,f, indent=4, ensure_ascii=False)
    
    with open("data/config.json","w") as f:
        json.dump(webhook,f, indent=4, ensure_ascii=False)

def cargar_datos():
    try:
        with open("data/datos_gestor.json", "r") as f:
            datos = json.load(f)
            
            tareas = []
            tareas_rutina = []

            for dato in datos["tareas"]:
                tarea = Tarea(dato["nombre"], dato["prioridad"])
                tarea.estado = dato["estado"]
                tarea.hora = dato["hora"]
                tareas.append(tarea)
            
            for dato in datos["rutinas"]:
                rutina = TareaRutina(dato["nombre"], dato["prioridad"])
                rutina.estado = dato["estado"]
                rutina.hora = dato["hora"]
                rutina.racha = dato["racha"]
                tareas_rutina.append(rutina)
            
            registro_cumplidos = datos["registro"]

        with open("data/historial.json", "r") as f: 
            historial = json.load(f)
        
        with open("data/puntaje.json", "r") as f: 
            puntos = json.load(f)
        
        with open("data/config.json", "r") as f: 
            webhook = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        tareas = []
        tareas_rutina = []
        historial = []
        registro_cumplidos = []
        webhook = ""
        puntos = 0
    return tareas,historial,puntos,tareas_rutina,registro_cumplidos,webhook
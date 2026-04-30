import json
import os 
from clases import Tarea, TareaRutina
os.makedirs("data", exist_ok=True)

def guardar_datos(tareas,historial,puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,id_canal): 

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
            "registro": registro_cumplidos,
            "Frases": lista_frases
        }, f, indent=4, ensure_ascii=False)

    with open("data/historial.json", "w") as f: 
        json.dump(historial,f, indent=4, ensure_ascii=False)
    
    with open("data/puntaje.json","w") as f:
        json.dump(puntos,f, indent=4, ensure_ascii=False)
    
    confi_data = {
        "webhook_url": webhook,
        "usar_frase_l": usar_frase,
        "token_j": token,
        "canal": id_canal
    }
    with open("data/config.json","w") as f:
        json.dump( confi_data, f, indent=4, ensure_ascii=False)

def cargar_datos():
    try:
        with open("data/datos_gestor.json", "r") as f:
            datos = json.load(f)

            lista_frases = datos["Frases"]
            tareas = []
            tareas_rutina = []

            for dato in datos["tareas"]:
                tarea = Tarea(dato["nombre"], dato["prioridad"])
                tarea.fecha_creacion = dato["creacion"]
                tarea.estado = dato["estado"]
                tarea.hora = dato["hora"]
                tareas.append(tarea)
            
            for dato in datos["rutinas"]:

                rutina = TareaRutina(dato["nombre"], dato["prioridad"])
                rutina.fecha_creacion = dato["creacion"]
                rutina.estado = dato["estado"]
                rutina.hora = dato["hora"]
                rutina.racha = dato["racha"]
                rutina.dias = dato["dias"]
                tareas_rutina.append(rutina)
            
            registro_cumplidos = datos["registro"]

        with open("data/historial.json", "r") as f: 
            historial = json.load(f)
        
        with open("data/puntaje.json", "r") as f: 
            puntos = json.load(f)
        
        with open("data/config.json", "r") as f: 
            confi_data = json.load(f)
            
            webhook = confi_data["webhook_url"]
            usar_frase = confi_data["usar_frase_l"]
            token = confi_data["token_j"]
            canal = confi_data["canal"]

    except (FileNotFoundError, json.JSONDecodeError):
        tareas = []
        tareas_rutina = []
        historial = []
        registro_cumplidos = []
        lista_frases = []
        webhook = ""
        usar_frase = True
        token = ""
        canal = ""
        puntos = 0
    return tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal
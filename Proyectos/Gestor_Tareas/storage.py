import json

def guardar_datos(tareas,historial,puntos): 
    with open("tareas.json","w") as f:  
        json.dump(tareas,f)

    with open("historial.json","w") as f:  
        json.dump(historial,f)
    
    with open("puntaje.json","w") as f:
        json.dump(puntos,f)

def cargar_datos():
    global tareas,historial, puntos
    try:
        with open("tareas.json","r") as f:
            tareas = json.load(f)
            
        with open("historial.json","r") as f:  
            historial = json.load(f)
        
        with open("puntaje.json","r") as f:
            puntos = json.load(f)

    except FileNotFoundError:
        tareas = []
        historial = []
        puntos = 0
    return tareas,historial,puntos
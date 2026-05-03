import json
import os 
import sys
import shutil
from clases import Tarea, TareaRutina

if getattr(sys, 'frozen', False):
    ruta_base = os.path.dirname(sys.executable)
else:
    ruta_base = os.path.dirname(os.path.abspath(__file__))

CARPETA_DATA = os.path.join(ruta_base, "data")
os.makedirs(CARPETA_DATA, exist_ok=True) # Usamos la variable pro, no "data" a secas

# Definimos las rutas de todos tus archivos usando la base
RUTA_GESTOR = os.path.join(CARPETA_DATA, "datos_gestor.json")
RUTA_HISTORIAL = os.path.join(CARPETA_DATA, "historial.json")
RUTA_PUNTOS = os.path.join(CARPETA_DATA, "puntaje.json")
RUTA_CONFIG = os.path.join(CARPETA_DATA, "config.json")
RUTA_BACKUP = os.path.join(CARPETA_DATA, "backup_completo.bak")

def guardar_datos(tareas,historial,puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,id_canal): 

    tareas_json = []
    for tarea in tareas:
        tareas_json.append(tarea.a_diccionario())

    tareas_rutina_json = []
    for rutina in tareas_rutina:
        tareas_rutina_json.append(rutina.a_diccionario())

    try:
        # Usamos las constantes que definimos arriba
        with open(RUTA_GESTOR, "w", encoding="utf-8") as f:
            json.dump({
                "tareas": tareas_json,
                "rutinas": tareas_rutina_json,
                "registro": registro_cumplidos,
                "Frases": lista_frases
            }, f, indent=4, ensure_ascii=False)

        with open(RUTA_HISTORIAL, "w", encoding="utf-8") as f: 
            json.dump(historial, f, indent=4, ensure_ascii=False)
        
        with open(RUTA_PUNTOS, "w", encoding="utf-8") as f:
            json.dump(puntos, f, indent=4, ensure_ascii=False)
        
        confi_data = {
            "webhook_url": webhook, "usar_frase_l": usar_frase,
            "token_j": token, "canal": id_canal
        }
        with open(RUTA_CONFIG, "w", encoding="utf-8") as f:
            json.dump(confi_data, f, indent=4, ensure_ascii=False)

        # BACKUP: Lo guardamos en la misma carpeta data pero con otra extensión
        # Así no dependes de rutas de tu carpeta personal
        shutil.copy2(RUTA_GESTOR, RUTA_BACKUP)
        
    except Exception as e:
        print(f"Error al guardar: {e}")

def cargar_datos():
    # 1. Usamos la constante RUTA_GESTOR
    if not os.path.exists(RUTA_GESTOR):
        print("Archivo no encontrado. Creando base de datos inicial...")
        return [], [], 0, [], [], "", [], True, "", ""
    
    try:
        # 2. IMPORTANTE: Cambiamos "data/..." por las constantes
        with open(RUTA_GESTOR, "r", encoding="utf-8") as f:
            datos = json.load(f)
            # ... (todo tu proceso de reconstrucción de objetos está perfecto) ...
            lista_frases = datos["Frases"]
            tareas = []
            tareas_rutina = []

            for dato in datos["tareas"]:
                tarea = Tarea(dato["nombre"], dato["prioridad"], dato["hora"])
                tarea.fecha_creacion = dato.get("creacion", "") # Usar .get evita errores si falta la clave
                tarea.estado = dato["estado"]
                tareas.append(tarea)
            
            for dato in datos["rutinas"]:
                rutina = TareaRutina(dato["nombre"], dato["prioridad"], dato["hora"], dato["dias"])
                rutina.fecha_creacion = dato.get("creacion", "")
                rutina.estado = dato["estado"]
                rutina.racha = dato.get("racha", 0)
                tareas_rutina.append(rutina)
            
            registro_cumplidos = datos["registro"]

        # 3. Seguimos usando las constantes para el resto
        with open(RUTA_HISTORIAL, "r", encoding="utf-8") as f: 
            historial = json.load(f)
        
        with open(RUTA_PUNTOS, "r", encoding="utf-8") as f: 
            puntos = json.load(f)
        
        with open(RUTA_CONFIG, "r", encoding="utf-8") as f: 
            confi_data = json.load(f)
            webhook = confi_data["webhook_url"]
            usar_frase = confi_data["usar_frase_l"]
            token = confi_data["token_j"]
            canal = confi_data["canal"]

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error cargando datos: {e}")
        # Valores por defecto en caso de fallo
        tareas, tareas_rutina, historial, registro_cumplidos, lista_frases = [], [], [], [], []
        webhook, usar_frase, token, canal, puntos = "", True, "", "", 0
        
    return tareas, historial, puntos, tareas_rutina, registro_cumplidos, webhook, lista_frases, usar_frase, token, canal
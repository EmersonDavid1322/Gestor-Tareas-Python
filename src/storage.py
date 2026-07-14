import json
import os 
import sys

if getattr(sys, 'frozen', False):
    ruta_base = os.path.dirname(sys.executable)
    CARPETA_DATA = os.path.join(ruta_base, "data")
else:
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    CARPETA_DATA = os.path.join(os.path.dirname(ruta_base), "data")

os.makedirs(CARPETA_DATA, exist_ok=True)

RUTA_FRASES = os.path.join(CARPETA_DATA, "frases.json")
RUTA_PUNTOS = os.path.join(CARPETA_DATA, "puntaje.json")
RUTA_CONFIG = os.path.join(CARPETA_DATA, "config.json")

def crear_archivos():
    archivos = {
        RUTA_FRASES: [],
        RUTA_PUNTOS: 0,
        RUTA_CONFIG: {
            "webhook_url": "",
            "usar_frase_l": True,
            "token_j": "",
            "canal": ""
        }
    }

    for ruta, contenido in archivos.items():
        if not os.path.exists(ruta):
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(contenido, f, indent=4, ensure_ascii=False)

def guardar_datos(puntos,webhook,lista_frases,usar_frase,token,id_canal): 
        
        with open(RUTA_FRASES, "w", encoding="utf-8") as f:
            json.dump(lista_frases, f, indent=4, ensure_ascii=False)

        with open(RUTA_PUNTOS, "w", encoding="utf-8") as f:
            json.dump(puntos, f, indent=4, ensure_ascii=False)
        
        confi_data = {
            "webhook_url": webhook, "usar_frase_l": usar_frase,
            "token_j": token, "canal": id_canal
        }
        with open(RUTA_CONFIG, "w", encoding="utf-8") as f:
            json.dump(confi_data, f, indent=4, ensure_ascii=False)

def cargar_datos():
    
    try:
        with open(RUTA_FRASES, "r", encoding="utf-8") as f: 
            lista_frases = json.load(f)

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
        lista_frases = []
        webhook, usar_frase, token, canal, puntos = "", True, "", "", 0
        
    return puntos, webhook, lista_frases, usar_frase, token, canal
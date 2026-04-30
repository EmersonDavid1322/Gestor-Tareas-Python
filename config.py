import requests
from discord_bot import on_ready

from storage import guardar_datos, cargar_datos
tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

def agregar_frase_nueva():
    nueva_frase = input("Introduce la nueva frase motivadora: ")
    
    if nueva_frase.strip():
        lista_frases.append(nueva_frase)
        
        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token)
        
        print(f"Frase guardada correctamente. Ahora tienes {len(lista_frases)} frases.")
    else:
        print("No puedes guardar una frase vacía.")

def opcion_frase():

    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, canal = cargar_datos()

    if usar_frase:
        print("La opción de enviar frases esta activa")
        opcion = input("¿Desea desactivarla? (S/N): ").lower()
        if opcion in ("s","si"):
            usar_frase = False
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
            print("Se desactivo la opción de enviar frases")
        else:
            print("No se hiso ningun cambio \n")
    else:
        print("La opción de enviar frases esta desactivada")
        opcion = input("¿Desea activarla? (S/N): ").lower()
        if opcion in ("s","si"):
            usar_frase = True
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)
            print("Se activo la opción de enviar frases")
        else:
            print("No se hiso ningun cambio \n")


def web_h():
    try:
        webhook = input("Introduzca su WEBHOOK_URL para poder notificar en discord: ")
        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,usar_frase,usar_frase,token,canal)
        confirmar = input("¿Desea probar su WEBHOOK_URL? (S/N): ").lower()
        if confirmar in ("s","si"):
            requests.post(webhook, json={"content": "Su WebHook funciona correctamente"})
            print("Se ha enviado un emnsaje de prueba a su WEBHOOK")

    except requests.exceptions.MissingSchema:
        print("❌ URL inválida. Falta https://")

    except requests.exceptions.InvalidURL:
        print("❌ URL inválida")

    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al webhook")

    except requests.exceptions.Timeout:
        print("❌ Tiempo de espera agotado")

    except requests.exceptions.RequestException:
        print("❌ Error al enviar prueba")
    return webhook


def token_bot_discord():
    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    if token == "" and canal == "":
        print("No hay ningun TOKEN guardado \nNO hay ningun id canal guardado \n")
        token = input("Introduzca el TOKEN de su bot: ").strip()
        canal = input("Introduzca el id del canal en que desea tener el bot: ").strip()
        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)

    else:
        confirmacion = input(f"Su token actualmente es {token} \nY su id canal actual es {canal} \n ¿Desea editarlo? (S/N): ").lower()
        if confirmacion in ("s","si"):
            token = input("Introduzca el TOKEN de su bot: ").strip()
            canal = input("Introduzca el id del canal en que desea tener el bot: ").strip()
            guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal)

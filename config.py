import requests
from storage import *

def web_h(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook):
    try:
        webhook = input("Introduzca su WEBHOOK_URL para poder notificar en discord: ")
        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook)
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

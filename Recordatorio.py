import requests
from storage import cargar_datos
import os
from datetime import datetime
<<<<<<< HEAD
import random
=======
>>>>>>> 16710cdeb4565ecf98a0ff2f7af30c8b0f7f803e
os.chdir("/home/emersondavid/Documentos/P/Phyton/Programa_De_Practica/Proyectos/Gestor_Tareas")

def revisar_y_enviar():
    try:
<<<<<<< HEAD
        tareas, historial, puntos, tareas_rutina,registro_cumplidos, webhook, lista_frases, usar_frase = cargar_datos()
=======
        tareas, historial, puntos, tareas_rutina,registro_cumplidos, webhook = cargar_datos()
>>>>>>> 16710cdeb4565ecf98a0ff2f7af30c8b0f7f803e
        hora_actual = datetime.now().strftime("%H:%M")
        pendientes = []
        for prioridad in ["Alta","Media","Baja"]:
            for t in tareas_rutina:
                if t.prioridad == prioridad and t.hora is not None and t.hora == hora_actual:
<<<<<<< HEAD
                    mensaje_pre = f"- {t.nombre} ({t.prioridad})({t.hora})"
                    if usar_frase:
                        if lista_frases:
                            eleccion = random.choice(lista_frases)
                            mensaje_pre += f"\n - */{eleccion}/*"
                        else:
                            mensaje_pre += f"\n - */La fortaleza del hombre radica en el dominio de su mente/*"
        pendientes.append(mensaje_pre)
        if pendientes:
            mensaje_texto = "Tareas pendientes:\n" + "\n".join(pendientes)
        else:
            return

        requests.post(webhook, json={"content": mensaje_texto})
    except IndexError:
        print("❌ No hay frase registradas")
    except requests.exceptions.MissingSchema:
        print("❌ URL inválida. Falta https://")

=======
                    pendientes.append(f"- {t.nombre} ({t.prioridad})({t.hora})")

        if pendientes:
            mensaje_texto = "Tareas pendientes:\n" + "\n".join(pendientes)
        else:
            return

        requests.post(webhook, json={"content": mensaje_texto})
    except requests.exceptions.MissingSchema:
        print("❌ URL inválida. Falta https://")

>>>>>>> 16710cdeb4565ecf98a0ff2f7af30c8b0f7f803e
    except requests.exceptions.InvalidURL:
        print("❌ URL inválida")

    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al webhook")

    except requests.exceptions.Timeout:
        print("❌ Tiempo de espera agotado")

    except requests.exceptions.RequestException:
        print("❌ Error al enviar prueba")


if __name__ == "__main__":
    revisar_y_enviar()
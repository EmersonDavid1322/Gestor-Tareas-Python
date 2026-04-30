import requests
from storage import cargar_datos
import os
from datetime import datetime
import random   
ruta_del_script = os.path.dirname(os.path.abspath(__file__))
os.chdir(ruta_del_script)

def revisar_y_enviar():
    try:
        fecha_hoy = datetime.now().strftime("%d/%m/%Y")
        hora_actual = datetime.now().strftime("%H:%M")
        pendientes = []
        tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

        dias_semana = ["lunes","martes","miércoles","jueves","viernes","sabado","domingo"]
        indice_hoy = datetime.now().weekday()
        dia_actual_texto = dias_semana[indice_hoy]
        
        for prioridad in ["Alta","Media","Baja"]:
            for t in tareas_rutina:
                if dia_actual_texto in t.dias:
                    if t.prioridad == prioridad and t.hora is not None and t.hora == hora_actual:
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
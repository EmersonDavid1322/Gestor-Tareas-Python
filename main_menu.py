from funciones import *
from config import *
from storage import cargar_datos
from sub_menus import *
<<<<<<< HEAD
tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase = cargar_datos()
=======
tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook = cargar_datos()
>>>>>>> 16710cdeb4565ecf98a0ff2f7af30c8b0f7f803e

while True:
    opcion = menu_f()
    
    if opcion == 1:
        gestor_tareas()
    elif opcion == 2:
        historial_f(historial)
    elif opcion == 3:
        estadisticas(tareas)
    elif opcion == 4:
<<<<<<< HEAD
        configuracion(tareas, historial,puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
=======
        configuracion()
>>>>>>> 16710cdeb4565ecf98a0ff2f7af30c8b0f7f803e
    elif opcion == 5:
        confirmacion = input("Ha seleccionado salir, ¿esta seguro? (S/N): ").lower()
        if confirmacion in ("s","si"):
            print("Ha salido")
            break
        else:
            print("Volviendo al menu")
    else:
        print("Seleccione una opción valida")


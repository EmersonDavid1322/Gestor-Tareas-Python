from funciones import *
from config import *
from storage import cargar_datos

tareas, historial, puntos, tareas_rutina, registro_cumplidos,config = cargar_datos()

while True:
    opcion = menu_f()
    
    if opcion == 1:
        agregar_tarea(tareas, historial, puntos,tareas_rutina,registro_cumplidos)
    elif opcion == 2:
        ver_tareas_registros(tareas,tareas_rutina,registro_cumplidos)
    elif opcion == 3:
        buscar_tarea(tareas,historial,puntos,tareas_rutina,registro_cumplidos)
    elif opcion == 4:
        editar_tarea(tareas,historial,puntos,tareas_rutina,registro_cumplidos)
    elif opcion == 5:
        puntos = marcar_tarea_completa(tareas, historial, puntos,tareas_rutina,registro_cumplidos)
    elif opcion == 6:
        ver_tareas_pendiente(tareas)
    elif opcion == 7:
        ver_tareas_completas(tareas,puntos)
    elif opcion == 8:
        historial_f(historial)
    elif opcion == 9:
        elimnar_tarea(tareas, historial, puntos,tareas_rutina,registro_cumplidos)
    elif opcion == 10:
        estadisticas(tareas)
    elif opcion == 11:
        web_h(tareas, historial, puntos,tareas_rutina,registro_cumplidos,config)
    elif opcion == 12:
        confirmacion = input("Ha seleccionado salir, ¿esta seguro? (S/N): ").lower()
        if confirmacion in ("s","si"):
            print("Ha salido")
            break
        else:
            print("Volviendo al menu")
    else:
        print("Seleccione una opción valida")


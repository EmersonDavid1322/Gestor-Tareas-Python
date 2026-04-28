from funciones import *
from storage import *
from config import *

tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase = cargar_datos()

def gestor_tareas():
    while True:
        try:
            print("-----Gestor Tareas-----")
            print("1) Crear una nueva tarea")
            print("2) Marcar tarea completa")
            print("3) Ver tareas")
            print("4) Buscar tarea")
            print("5) Editar tarea")
            print("6) Eliminar tarea")
            print("7) Volver al Menu Principal")

            opcion = int(input("\nSelecciona una opción: "))

        except ValueError:
            print("Debe ingresar un valor numerico")
            continue
        
        if opcion == 1:
            agregar_tarea(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
        
        elif opcion == 2:
            marcar_tarea_completa(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
        elif opcion == 3:
            try:
                print("1) ver tareas pendientes \t 2) ver tareas completas \n")
                print("3) Ver listado de tareas o registro de rutinas")

                opcion_ver = int(input("\nSeleccione una opción: "))
            except ValueError:
                print("Debe de ingresas un valor numerico")
            
            if opcion_ver == 1:
                ver_tareas_pendiente(tareas)
            elif opcion_ver == 2:
                ver_tareas_completas(tareas,puntos)
            else:
                ver_tareas_registros(tareas,tareas_rutina,registro_cumplidos)
        
        elif opcion == 4:
            buscar_tarea(tareas, historial,puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
        
        elif opcion == 5:
            editar_tarea(tareas, historial,puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
        
        elif opcion == 6:
            elimnar_tarea(tareas, historial,puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase)
        
        elif opcion == 7:
            print("Volviendo al Menu Principal...\n")
            return
        else:
            print("Valor no valido")


def configuracion():

    while True:
        try:
            print("-----Configuraciones-----")
            print("1) Configurar WEBHOOK")
            print("2) Editar lista de frases")
            print("3) Desactivar/Activar frases")
            print("4) Salir")

            opcion = int(input("\nSeleccione una opción: "))
        except ValueError:
            print("Debe de ingresas un valor numerico")
            continue

        if opcion == 1:
            tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook,lista_frases,usar_frase = cargar_datos()

            if webhook == "":
                print("No hay WEBHOOK registrado \n")
                web_h()
            else:
                confirmacion = input(f"Su webhook actual es: \n{webhook} \n¿Desea editarlo? (S/N): ").lower()
                if confirmacion in ("s","si"):
                    web_h()
        
        elif opcion == 2:
            agregar_frase_nueva()
        
        elif opcion == 3:
            opcion_frase()
            print("Opción aun no implementada\n")
        
        elif opcion == 3:
            print("Opcion aun no implementada\n")
        
        elif opcion == 4:
            return
        
        else:
            print("Valor no valido")
